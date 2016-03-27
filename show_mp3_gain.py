import sys
import subprocess
import itunes


playlist_name = sys.argv[1].decode('utf-8')
tunes = itunes.ITunes()

playlist = tunes[playlist_name]

for track in playlist.tracks:
    print track.title
    path = track.path
    if path.endswith('.mp3'):
        subprocess.call(['mp3gain', path])
