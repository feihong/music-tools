"""
Copy all the tracks in tracks.json to the given directory
"""
from pathlib import Path
import json
import shutil
import sys

output_dir = Path(sys.argv[1]).expanduser()
if not output_dir.exists():
  output_dir.mkdir(parents=True)

tracks_file = Path('tracks.json')
shutil.copy(tracks_file, output_dir / tracks_file.name)

tracks = json.loads(tracks_file.read_bytes())

for i, track in enumerate(tracks, 1):
  input_file = Path(track['location'])
  output_file = output_dir / input_file.name
  print(f'{i}. {output_file}')
  shutil.copy(input_file, output_file)

print(f'\nCopied {i} items')
