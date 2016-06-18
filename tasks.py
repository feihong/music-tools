import os.path as op
import codecs
import shutil
import subprocess
from collections import defaultdict
import itertools
from datetime import datetime
import random

from invoke import run, task
from mako.template import Template

import itunes


@task
def print_favorite_songs():
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

    for genre, tuples in songs.iteritems():
        print_(u'%s:' % genre)
        for title, artist in tuples:
            print_(u'%s ~> %s' % (artist, title))
        print

    print_('\nListed %d songs' % count)


@task
def print_popular_songs():
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

    artists = artists.items()
    artists.sort(key=lambda x: len(x[1].songs), reverse=True)

    for artist, info in artists:
        print_(u'%s (%s):' % (artist, info.genre))
        print_('- ' + u'\n- '.join(info.songs) + '\n')

    print_('\nListed %d artists' % len(artists))


@task
def show_mp3_gain(playlist):
    tunes = itunes.ITunes()
    playlist = tunes[playlist]

    for track in playlist.tracks:
        print track.title
        path = track.path
        if path.endswith('.mp3'):
            subprocess.call(['mp3gain', path])


@task
def copy_playlist_files(playlist, dest_dir, start=None, stop=None):
    """
    Given the name of a playlist and a directory, copy all songs from the playlist
    into that directory, and also generate a text file containing the lyrics of all
    the songs in the playlist.

    """
    lyrics_path = op.join(dest_dir, 'lyrics.html')

    if start is not None:
        start = int(start) - 1
    if stop is not None:
        stop = int(stop)

    lyric_tracks = []

    for track in get_tracks(playlist, start, stop):
        path = track.path
        output_path = op.join(dest_dir, op.basename(path))
        shutil.copy(path, output_path)
        print '%s - %s' % (track.title, track.artist)
        if track.lyrics:
            lyric_tracks.append(track)

    with codecs.open(lyrics_path, 'w', 'utf-8') as fp:
        tmpl = Template(HTML_TEMPLATE)
        fp.write(tmpl.render(tracks=lyric_tracks))


@task
def copy_tracks_newer_than(date, dest_dir):
    """
    Copy music files newer than the given date to the specified directory.
    Accepts date strings in the form YYYY-mm-dd.

    """
    start_date = datetime.strptime(date, '%Y-%m-%d')
    tunes = itunes.ITunes()
    count = 0
    for track in tunes.tracks:
        if track.date_added >= start_date:
            print track.title
            shutil.copy(track.path, dest_dir)
            count += 1
    print 'Copied %d tracks to %s' % (count, dest_dir)


@task
def new_playlist(name, duration):
    """
    Create a new playlist of random songs rated 4 stars or above, lasting at
    least the given duration (in hours).

    """
    # Convert to seconds.
    duration = float(duration) * 3600
    tunes = itunes.ITunes()

    playlist = tunes.add_playlist(name)

    results = {}
    curr_duration = 0
    num = 1

    tracks = [t for t in tunes.tracks if t.stars >= 4]
    print len(tracks)

    while True:
        track = random.choice(tracks)
        if track.unique_id not in results:
            results[track.unique_id] = track
            playlist.add_track(track)
            curr_duration += track.duration
            num += 1
            print num, track.title, curr_duration
            if curr_duration > duration:
                break

    print 'Added %d tracks to %s' % (len(results), name)


HTML_TEMPLATE = """\
<!doctype html>
<html class="no-js" lang="">
<head>
<meta charset="utf-8">
<meta http-equiv="x-ua-compatible" content="ie=edge">
<title>Lyrics</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>

<h1>Lyrics</h1>

% for track in tracks:
    <div>
        <h2>${track.title}</h2>
        <h3>${track.artist}</h3>

        <div>
            <audio controls>
                <source src='${track.filename}'>
            </audio>
        </div>

        <div>
        % for line in track.lyrics.splitlines():
            ${line}<br>
        % endfor
        </div>
    </div>
% endfor
</body>
</html>
"""


def get_tracks(playlist_name, start=None, stop=None):
    import itunes
    tunes = itunes.ITunes()
    if not isinstance(playlist_name, unicode):
        playlist_name = playlist_name.decode('utf-8')
    playlist = tunes[playlist_name]
    for track in itertools.islice(playlist.tracks, start, stop):
        yield track


def print_(s):
    """
    When printing to stdout, you need to encode to utf-8 or else you won't be
    able to redirect to a file.

    """
    if isinstance(s, unicode):
        print s.encode('utf-8')
    else:
        print s
