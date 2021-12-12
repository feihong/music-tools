"""
List tracks whose files can't be found
"""
import json
from pathlib import Path

count = 0

for track in json.load(open('tracks.json')):
  path = Path(track['location'])
  if not path.exists():
    print(track['title'], path)
    count += 1

print(f'There were {count} tracks whose files could not be found')
