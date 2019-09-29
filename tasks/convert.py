import subprocess
import tempfile
from pathlib import Path

from invoke import task
import itunes


@task
def to_m4a(ctx, mp3_file):
  """
  Convert mp3 file to m4a format

  """
  mp3_file = Path(mp3_file)
  if mp3_file.suffix == '.m4a':
    print(f'{mp3_file} is already in m4a format')
    return

  output_file = Path(mp3_file.stem).with_suffix('.m4a')

  cmd = [
    'ffmpeg',
    '-y',                   # overwrite existing file
    '-i', str(mp3_file),
    '-c:a', 'libfdk_aac',   # use best encoder
    '-vbr', '2',            # use high quality
    str(output_file)
  ]
  subprocess.call(cmd)

  print(f'Generated {output_file}')
