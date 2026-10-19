import argparse
import json
from pathlib import Path
from common import read_json, style_for, validate, write_json

def compile_prompt(deck, page):
    style = style_for(deck['style'])
    parts = [
        'Create one flat presentation slide. Follow the selected style and exact copy below.',
        f"Language: {deck['language']}. Canvas: 16:9. Page {page['page']}/{deck['slide_count']} (metadata, not extra visible copy).",
        'SELECTED STYLE (visual guidance only):',
        json.dumps(style, ensure_ascii=False, indent=2),
        'LAYOUT (do not render these instructions):', page['layout'],
        'Suggested imagery: ' + '; '.join(page.get('visual_elements', [])),
        'EXACT VISIBLE COPY (render these strings only; preserve numbers and capitalization):',
        json.dumps(page['visible_text'], ensure_ascii=False, indent=2),
        'Do not render source notes, metadata, layout instructions, or an additional slogan.',
        'No invented facts or numbers. Do not copy people, logos, project names or claims from a style reference.',
        'Use clear type; keep labels inside their bounds. Follow any specified process order exactly.',
    ]
    if page.get('preserve_pixels'):
        parts += [
            'Leave a calm image slot at normalized [left, top, width, height]: ' + json.dumps(page['image_box']),
            'Do not synthesize the source screenshot or photo. The original will be inserted afterward.'
        ]
    return '\n\n'.join(parts) + '\n'

def main():
    parser = argparse.ArgumentParser(description='Compile prompts using exactly one selected style.')
    parser.add_argument('spec')
    parser.add_argument('--out-dir', required=True)
    args = parser.parse_args()
    try:
        deck = validate(read_json(args.spec))
        out = Path(args.out_dir)
        if out.exists() and any(out.iterdir()):
            raise ValueError('Use a new or empty output directory')
        out.mkdir(parents=True, exist_ok=True)
        for p in deck['slides']:
            (out / f"P{p['page']:02d}.txt").write_text(compile_prompt(deck, p), encoding='utf-8')
        write_json(out / 'deck.json', deck)
    except (ValueError, OSError) as exc:
        parser.exit(1, f'Prompt build failed: {exc}\n')
    print(f"Built {len(deck['slides'])} prompts. No network requests made.")

if __name__ == '__main__':
    main()
