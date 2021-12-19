from pathlib import Path
import mutagen.mp3

def get_mp3s():
  root_dir = Path('~/Music').expanduser()
  for f in root_dir.glob('**/*.mp3'):
    try:
      yield mutagen.File(str(f))
    except:
      print(f'{f} does not seem to be valid MP3 file')

title_tags = set()
lyrics_tags = set()

for mp3 in get_mp3s():
  for key in mp3.tags.keys():
    if key.startswith('USLT'):
      lyrics_tags.add(key)
    if key.startswith('TIT'):
      title_tags.add(key)

# Only one that should appear is USLT::eng
print('Lyrics tags:', ', '.join(lyrics_tags))

print('Title tags:', ', '.join(title_tags))
