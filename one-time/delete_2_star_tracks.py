"""
Delete 2 star tracks
"""
import json
import os
from pathlib import Path

with open('tracks-2-stars.json') as fp:
  tracks = json.load(fp)
  confirm = input(f'Will delete {len(tracks)} files. Continue? ')

  for track in tracks:
    path = Path(track['location'])
    if not path.exists():
      print(f'{path} does not exist!')
      break
    print(path.exists(), path)
    # os.remove(path)
