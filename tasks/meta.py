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
                date_added=track.date_added,
            )

    output_path = Path('metadata.json')
    with output_path.open('w') as fp:
        for obj in gen():
            fp.write(json.dumps(obj) + '\n')
