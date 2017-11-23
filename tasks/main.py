import random
from collections import defaultdict

import itunes
from invoke import run, task


@task
def print_favorite_songs(ctx):
    """
    Print all 5-star songs, grouped by genre.

    """
    # Map genre to songs
    songs = defaultdict(list)

    tunes = itunes.ITunes()

    great_tracks = (t for t in tunes.tracks if t.stars == 5)
    count = 0
    for t in great_tracks:
        songs[t.genre].append((t.title, t.artist))
        count += 1

    for genre, tuples in songs.items():
        print(f'{genre}:')
        for title, artist in tuples:
            print(f'{artist} ~> {title}')
        print

    print(f'\nListed {count} songs')


@task
def print_popular_songs(ctx):
    """
    Print songs rated 4 stars or above, grouped by artist.

    """
    class ArtistInfo:
        def __init__(self):
            self.genre = None
            self.songs = []

    # Map artists to ArtistInfo
    artists = defaultdict(ArtistInfo)

    tunes = itunes.ITunes()

    good_tracks = (t for t in tunes.tracks if t.stars >= 4)
    for t in good_tracks:
        info = artists[t.artist]
        info.genre = t.genre
        info.songs.append(t.title)

    artists = list(artists.items())
    artists.sort(key=lambda x: len(x[1].songs), reverse=True)

    for artist, info in artists:
        print(f'{artist} ({info.genre}):')
        print('- ' + '\n- '.join(info.songs) + '\n')

    print(f'\nListed {len(artists)} artists')


@task
def new_playlist(ctx, name, duration):
    """
    Create a new playlist of random songs rated 4 stars or above, lasting at
    least the given duration (in hours).

    """
    # Convert from hours to seconds.
    duration = float(duration) * 3600
    tunes = itunes.ITunes()

    playlist = tunes.add_playlist(name)

    results = {}
    curr_duration = 0
    num = 1

    tracks = [t for t in tunes.tracks if t.stars >= 4]
    print(f'Number of 4+ rated tracks: {len(tracks)}')

    while True:
        track = random.choice(tracks)
        if track.unique_id not in results:
            results[track.unique_id] = track
            playlist.add_track(track)
            curr_duration += track.duration
            num += 1
            print(f'{num} {track.title} {curr_duration}')
            if curr_duration > duration:
                break

    print(f'Added {len(results)} tracks to {name}')
