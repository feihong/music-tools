from pathlib import Path
import mutagen.mp4
import collections

def get_m4as():
  root_dir = Path('~/Music').expanduser()
  for f in root_dir.glob('**/*.m4a'):
    try:
      yield mutagen.mp4.MP4(str(f))
    except:
      print(f'{f} does not seem to be valid AAC file')

image_formats = collections.defaultdict(list)

for m4a in get_m4as():
  covers = m4a.get('covr', [])
  if len(covers) > 1:
    print(f'{m4a.filename} has more than one cover')

  try:
    format = covers[0].imageformat
    if format == mutagen.mp4.MP4Cover.FORMAT_JPEG:
      key = 'jpeg'
    elif format == mutagen.mp4.MP4Cover.FORMAT_PNG:
      key = 'png'

    image_formats[key].append(m4a.filename)
  except:
    pass

for k, v in image_formats.items():
  print(f'{k} -> {len(v)}')

print('\nFiles with PNG artwork:')
for i, f in enumerate(image_formats['png'], 1):
  print(f'{i}. {f}')

