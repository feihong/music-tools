from pathlib import Path
import json
from invoke import task
import itunes


@task
def export(ctx):
    """
    Export rating and date-added metadata

    """
    def gen():
        tracks = itunes.ITunes().tracks
        for i, track in enumerate(tracks, 1):
            print(f'{i} {track.title} - {track.artist}')
            yield dict(
                title=track.title,
                artist=track.artist,
                rating=track.rating,
            )

    output_path = Path('metadata.json')
    with output_path.open('w') as fp:
        for obj in gen():
            fp.write(json.dumps(obj) + '\n')


@task
def import_meta(ctx, input_file):
    """
    Import metadata from the given file

    """
    tmap = _create_track_map()
    def gen():
        input_path = Path(input_file)
        with input_path.open() as fp:
            for line in fp:
                if line:
                    yield json.loads(line)

    for meta in gen():
        key = (meta['title'], meta['artist'])
        track = tmap.get(key)
        _track = track._track
        _track.setRating_(meta['rating'])



def _create_track_map():
    def gen():
        for track in itunes.ITunes.tracks:
            key = (track.title, track.artist)
            yield key, track

    return dict(gen())
