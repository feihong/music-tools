import subprocess
from invoke import task
import itunes


@task
def show_gain(ctx, playlist):
    tunes = itunes.ITunes()
    playlist = tunes[playlist]

    for track in playlist.tracks:
        print(track.title)
        path = track.path
        if path.endswith('.mp3'):
            subprocess.call(['mp3gain', path])
