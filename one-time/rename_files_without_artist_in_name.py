"""
Rename files that don't have the artist in the name and have no
"""
import json
from pathlib import Path
import re

def get_tracks():
  with open('tracks.json') as fp:
    tracks = json.load(fp)
    for track in tracks:
      path = Path(track['location'])
      if max(ord(c) for c in path.stem) > 255:
        continue
      if not re.match(r'2012-1[012]', path.parent.name):
        continue
      if not track['artist'] in path.stem:
        yield track

for i, track in enumerate(get_tracks(), 1):
  path = Path(track['location'])
  new_path = path.with_stem(f"{track['artist']}  {track['title']}".replace('/', '|'))
  path.rename(new_path)
  print(f"{i}. {path}, {new_path}")
