"""Heuristic public-source checks, not a comprehensive secret scanner."""
import re
from pathlib import Path
import sys
from common import ROOT, read_json, validate

def check(root):
    errors=[]
    required=['LICENSE','SKILL.md','README.md','README.en.md','config.example.json','.env.example','.gitignore']
    for name in required:
        if not (root/name).is_file():errors.append('Missing '+name)
    ignored_dirs={'.git','.venv','venv','__pycache__','work','outputs','.pytest_cache'}
    for path in root.rglob('*'):
        rel=path.relative_to(root)
        if any(p in ignored_dirs for p in rel.parts) or not path.is_file():continue
        if path.name == 'config.json' or (path.name.startswith('.env') and path.name!='.env.example'):
            errors.append('Private configuration present: '+str(rel));continue
        if path.suffix.lower() in {'.pptx','.pdf','.zip','.log','.ttf','.otf','.pem'}:
            errors.append('Unexpected binary/log/private asset: '+str(rel));continue
        try:text=path.read_text(encoding='utf-8-sig')
        except UnicodeDecodeError:
            errors.append('Unreviewed binary file: '+str(rel));continue
        if re.search(r'\b[A-Za-z]:[\\/](?:Users|PPTskill|PPT模板)[\\/]',text):errors.append('Machine-specific path: '+str(rel))
        if re.search(r'\bsk-[A-Za-z0-9_-]{20,}',text):errors.append('Possible literal key: '+str(rel))
        if path.suffix=='.md':
            # Relative links only. Skip external URLs, anchors and fenced placeholders.
            for target in re.findall(r'\]\(([^)]+)\)',text):
                if '://' in target or target.startswith('#'):continue
                target=target.split('#',1)[0]
                if target and not (path.parent/target).exists():errors.append('Broken link in '+str(rel)+': '+target)
    for spec in (root/'examples').glob('*.json'):
        try:validate(read_json(spec))
        except ValueError as exc:errors.append(str(exc))
    front=(root/'SKILL.md').read_text(encoding='utf-8-sig')
    if not front.startswith('---\nname: ppt-elegance-skill\n'):errors.append('Unexpected Skill frontmatter')
    if 'MIT License' not in (root/'LICENSE').read_text():errors.append('Missing MIT license')
    return errors

if __name__=='__main__':
    issues=check(ROOT)
    if issues:print('\n'.join(issues));sys.exit(1)
    print('Release source checks passed. Review actual staged files and Git history separately.')
