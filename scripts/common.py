"""Shared, provider-independent specification validation. Python 3.10+."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODES = {'technical', 'activity', 'innovation', 'medical', 'heritage'}
LAYOUTS = {'cover', 'background', 'goals', 'architecture', 'process', 'timeline',
           'comparison', 'photo-story', 'quote', 'results', 'screenshot',
           'evaluation', 'next-steps', 'closing'}
EVIDENCE = {'confirmed', 'supplied-quote', 'synthetic-demo', 'placeholder', 'unverified'}

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def safe_id(value):
    return isinstance(value, str) and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', value)

def style_for(name):
    if not safe_id(name):
        raise ValueError('style must be a lowercase hyphenated ID')
    path = ROOT / 'styles' / (name + '.json')
    if not path.is_file():
        raise ValueError(f'Unknown style: {name}')
    return read_json(path)

def validate(deck):
    if not isinstance(deck, dict):
        raise ValueError('Deck must be an object')
    for k in ('title', 'language'):
        if not isinstance(deck.get(k), str) or not deck[k].strip():
            raise ValueError(f'{k} must be a non-empty string')
    if deck.get('mode') not in MODES:
        raise ValueError('Unknown content mode')
    style_for(deck.get('style'))
    if deck.get('aspect_ratio') != '16:9':
        raise ValueError('This release supports aspect_ratio 16:9')
    pages = deck.get('slides')
    if not isinstance(pages, list) or not pages:
        raise ValueError('slides must be a non-empty list')
    if type(deck.get('slide_count')) is not int or deck['slide_count'] != len(pages):
        raise ValueError('slide_count must equal the number of slides')
    for n, page in enumerate(pages, 1):
        if not isinstance(page, dict) or type(page.get('page')) is not int or page['page'] != n:
            raise ValueError('Page numbers must be sequential from 1')
        if page.get('type') not in LAYOUTS:
            raise ValueError(f'Page {n}: unknown layout type')
        for k in ('title', 'layout', 'key_message'):
            if not isinstance(page.get(k), str) or not page[k].strip():
                raise ValueError(f'Page {n}: {k} must be non-empty text')
        visible = page.get('visible_text')
        if not isinstance(visible, list) or not visible or not all(isinstance(t, str) and t.strip() for t in visible):
            raise ValueError(f'Page {n}: visible_text must be a non-empty list of text')
        if page['title'] not in visible:
            raise ValueError(f'Page {n}: title must occur in visible_text')
        if page.get('evidence_status') not in EVIDENCE:
            raise ValueError(f'Page {n}: unknown evidence status')
        for k in ('source_basis', 'visual_elements'):
            if not isinstance(page.get(k, []), list) or not all(isinstance(t, str) for t in page.get(k, [])):
                raise ValueError(f'Page {n}: {k} must be a text list')
        for k in ('speaker_notes', 'source_image', 'image'):
            if k in page and not isinstance(page[k], str):
                raise ValueError(f'Page {n}: {k} must be text')
        if 'reviewed' in page and type(page['reviewed']) is not bool:
            raise ValueError(f'Page {n}: reviewed must be boolean')
        if 'preserve_pixels' in page and type(page['preserve_pixels']) is not bool:
            raise ValueError(f'Page {n}: preserve_pixels must be boolean')
        if page.get('preserve_pixels') and not page.get('source_image'):
            raise ValueError(f'Page {n}: preserve_pixels requires source_image')
        if 'image_box' in page:
            box = page['image_box']
            if (not isinstance(box, list) or len(box) != 4
                    or any(type(x) not in (int, float) for x in box)):
                raise ValueError(f'Page {n}: image_box must be [left, top, width, height]')
            x, y, w, h = box
            if not (x >= 0 and y >= 0 and w > 0 and h > 0 and x+w <= 1 and y+h <= 1):
                raise ValueError(f'Page {n}: image_box must fit normalized canvas')
        if page.get('preserve_pixels') and 'image_box' not in page:
            raise ValueError(f'Page {n}: preserve_pixels requires image_box')
    return deck
