"""
Generate json file for all the music files in the user's Music directory
"""
import sys
import mutagen.mp3, mutagen.mp4
import json
import itertools
from pathlib import Path

root_dir = Path('~/Music').expanduser()

# music_files = itertools.chain(root_dir.glob('**/*.mp3'), root_dir.glob('**/*.m4a'))
music_files = itertools.chain(root_dir.glob('**/*.m4a'))

def get_dict(input_file: Path):
  suffix = input_file.suffix
  if suffix == '.mp3':
    return get_dict_from_mp3(input_file)
  elif suffix == '.m4a':
    return get_dict_from_mp4(input_file)

def get_dict_from_mp3(music_file: Path):
  location = str(music_file)
  m = mutagen.mp3.MP3(location)
  lyrics = m.get('USLT::eng')
  if lyrics is not None:
    lyrics = lyrics.text
  return dict(
    title=m['TIT2'].text[0],
    artist=m['TPE1'].text[0],
    genre=m['TCON'].text[0],
    lyrics=lyrics,
    location=location,
  )

def get_dict_from_mp4(music_file: Path):
  location = str(music_file)
  m = mutagen.mp4.MP4(location)
  try:
    return dict(
      title=m['©nam'][0],
      artist=m['©ART'][0],
      genre=m.get('©gen', [''])[0],
      lyrics=m.get('©lyr', [''])[0],
      location=location,
    )
  except KeyError as err:
    print(f'{music_file} is missing a required field: {err}')
    sys.exit(1)

def get_dicts(music_files):
  for f in music_files:
    yield get_dict(f)

dicts = get_dicts(music_files)
# for d in dicts:
#   print(d)

with open('tracks.json', 'w') as fp:
  json.dump(list(dicts), fp, indent=2, ensure_ascii=False)
