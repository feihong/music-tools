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


@task
def songs_without_lyrics(ctx, playlist_name):
    """
    Show all songs without lyrics

    """
    tunes = itunes.ITunes()
    playlist = tunes[playlist_name]

    total_count = 0
    count = 0
    for track in playlist.tracks:
        total_count += 1
        if track.lyrics is None or track.lyrics.strip() == '':
            count += 1
            print(f'{count}. {track.artist}  {track.title}')

    print(f'\nFound {count} out of {total_count} songs without lyrics')
