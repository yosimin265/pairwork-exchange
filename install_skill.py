"""Explicit project-local skill installation; no global settings changed."""
from pathlib import Path
import argparse, shutil
p=argparse.ArgumentParser();p.add_argument('--target',choices=['codex','claude'],required=True);p.add_argument('--project',type=Path,required=True);a=p.parse_args()
d=a.project/('.agents' if a.target=='codex' else '.claude')/'skills'/'pairwork'
if d.exists():raise SystemExit(f'Already exists: {d}; inspect it before replacing.')
shutil.copytree(Path(__file__).parent/'skills'/'pairwork',d,ignore=shutil.ignore_patterns('.session.json','__pycache__'))
print(f'Installed: {d}. Open the project in your AI client, then ask to connect PairWork.')
