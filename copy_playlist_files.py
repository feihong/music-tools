import sys
import shutil
import os.path as op
import itunes


playlist_name = sys.argv[1].decode('utf-8')
output_dir = sys.argv[2]

tunes = itunes.ITunes()

playlist = tunes[playlist_name]

for track in playlist.tracks:
    path = track.path
    output_path = op.join(output_dir, op.basename(path))
    shutil.copy(path, output_path)
    print '%s - %s' % (track.title, track.artist)
