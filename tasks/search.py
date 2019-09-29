from invoke import task
import itunes


@task
def search_songs(ctx, keyword):
    """
    Search for given keyword in all songs

    """
    tunes = itunes.ITunes()

    count = 0
    for track in tunes.tracks:
        if keyword in track.title or keyword in track.artist or \
           (track.lyrics is not None and keyword in track.lyrics):
           count += 1
           print(f'{track.title} - {track.artist}')

    print(f'\nFound {count} songs')

