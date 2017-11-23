from mako.template import Template
from invoke import task


@task
def playlist_files(ctx, playlist, dest_dir, start=None, stop=None):
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
        print(f'{track.title} - {track.artist}')
        if track.lyrics:
            lyric_tracks.append(track)

    with codecs.open(lyrics_path, 'w', 'utf-8') as fp:
        tmpl = Template(HTML_TEMPLATE)
        fp.write(tmpl.render(tracks=lyric_tracks))


@task
def tracks_newer_than(ctx, date, dest_dir):
    """
    Copy music files newer than the given date to the specified directory.
    Accepts date strings in the form YYYY-mm-dd.

    """
    start_date = datetime.strptime(date, '%Y-%m-%d')
    tunes = itunes.ITunes()
    count = 0
    for track in tunes.tracks:
        if track.date_added >= start_date:
            print(track.title)
            shutil.copy(track.path, dest_dir)
            count += 1
    print(f'Copied {count} tracks to {dest_dir}')


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
