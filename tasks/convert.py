import subprocess
import tempfile
from pathlib import Path
import shutil

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

  cmd = [
      'mp3gain',
      # Apply Track gain automatically (all files set to equal loudness)
      '-r',
      # Automatically lower Track/Album gain to not clip audio
      '-k',
      str(mp3_file),
  ]
  subprocess.call(cmd)

  output_file = Path(mp3_file.stem).with_suffix('.m4a')

  cmd = [
    'ffmpeg',
    '-y',                   # overwrite existing file
    '-i', str(mp3_file),
    '-vn',                  # ignore video/image
    '-c:a', 'libfdk_aac',   # use best encoder
    '-vbr', '2',            # use high quality
    str(output_file)
  ]
  subprocess.call(cmd)

  print(f'Generated {output_file}')


@task
def to_mp4(ctx, m4a_file):
  """
  Convert m4a audio file to mp4 movie

  """
  m4a_file = Path(m4a_file)
  if m4a_file.suffix == '.mp4':
    print(f'{m4a_file} is already in mp4 format')
    return

  output_file = Path(m4a_file.stem).with_suffix('.mp4')
  image_file_initial = Path(m4a_file.parent) / (m4a_file.stem + '_artwork_1.jpg')
  image_file = Path(m4a_file.stem).with_suffix('.jpg')

  if not image_file.exists():
    cmd = [
      'AtomicParsley',
      str(m4a_file),
      '--extractPix'
    ]
    subprocess.call(cmd)

    shutil.move(image_file_initial, image_file)

  # Source: https://apple.stackexchange.com/a/107786
  cmd = [
    'ffmpeg',
    '-y',                   # overwrite existing file
    '-loop', '1',           # loop image infinitely
    '-i', str(image_file),
    '-i', str(m4a_file),
    '-c:a', 'copy',         # don't re-encode audio
    '-c:v', 'libx264',
    '-crf', '20',           # set constant rate factor to medium (0-51, 0 is lossless)
    '-pix_fmt', 'yuv420p',  # if not provided, will use yuv444p, which is not as widely supported
    '-shortest',            # needed to finish encoding after the audio stream finishes
    str(output_file)
  ]
  subprocess.call(cmd)

  print(f'Generated {output_file}')
