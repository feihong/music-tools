"""
Put all tracks into month folders of the format YYYY-MM
"""
import re
from pathlib import Path
import json
import shutil

def get_tracks():
  with open('tracks.json') as fp:
    tracks = json.load(fp)
    for track in tracks:
      location = Path(track['location'])
      if not location.exists():
        continue
      if re.match(r'\d{4}-\d{2}', location.parent.stem):
        continue
      yield track

music_dir = Path('~/Music/hanyu').expanduser()

for i, track in enumerate(get_tracks(), 1):
  target_dir = music_dir / track['added'][:7]
  if not target_dir.exists():
    target_dir.mkdir()

  suffix = Path(track['location']).suffix
  name = f'{track["artist"]}  {track["title"]}'.replace('/', '|')
  target_file = target_dir / f'{name}{suffix}'
  print(f'{i}. Move {track["location"]} to {target_file}')

  shutil.move(track['location'], target_file)
