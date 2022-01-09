"""
Copy all the tracks in tracks.json to ~/export/music, organized into folders based on their star ratings.
"""
from pathlib import Path
import json
import shutil

output_root_dir = Path('~/export/music').expanduser()
if not output_root_dir.exists():
  output_root_dir.mkdir(parents=True)

tracks_file = Path('tracks.json')
shutil.copy(tracks_file, output_root_dir / tracks_file.name)

tracks = json.loads(tracks_file.read_bytes())

for i, track in enumerate(tracks, 1):
  rating = track['rating']
  rating_dir = output_root_dir / f'{rating} star'
  if not rating_dir.exists():
    rating_dir.mkdir()

  input_file = Path(track['location'])
  output_file = rating_dir / input_file.name
  print(f'{i}. {output_file}')
  shutil.copy(input_file, output_file)

print(f'\nProcessed {i} items')
