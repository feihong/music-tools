"""
Convert all .m4a files in ~/Downloads to .mp4 video files
"""
import subprocess
from pathlib import Path
import mutagen.mp4
from mutagen.mp4 import MP4Cover


input_dir = Path('~/Downloads').expanduser()
m4a_files = input_dir.glob('*.m4a')

def convert(m4a_file):
  output_file = m4a_file.with_suffix('.mp4')
  if output_file.exists():
    return

  mp4 = mutagen.mp4.MP4(m4a_file)
  # Assume input file always has cover art
  cover = mp4['covr'][0]
  if cover.imageformat == MP4Cover.FORMAT_JPEG:
    suffix = '.jpg'
  elif cover.imageformat == MP4Cover.FORMAT_PNG:
    suffix = '.png'

  image_file = m4a_file.with_suffix(suffix)
  image_file.write_bytes(cover)

  # Source: https://apple.stackexchange.com/a/107786
  cmd = [
    'ffmpeg',
    '-y',                   # overwrite existing file
    '-loop', '1',           # loop image infinitely
    '-i', image_file,
    '-i', m4a_file,
    '-c:a', 'copy',         # don't re-encode audio
    '-c:v', 'libx264',
    '-crf', '20',           # set constant rate factor to medium (0-51, 0 is lossless)
    '-pix_fmt', 'yuv420p',  # if not provided, will use yuv444p, which is not as widely supported
    '-shortest',            # needed to finish encoding after the audio stream finishes
    output_file,
  ]
  subprocess.run(cmd)

  print(f'Generated {output_file}')

for m4a_file in m4a_files:
  convert(m4a_file)
