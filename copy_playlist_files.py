"""
Given the name of a playlist and a directory, copy all songs from the playlist
into that directory, and also generate a text file containing the lyrics of all
the songs in the playlist.

"""

import sys
import shutil
import codecs
import os.path as op


def main():
    playlist_name = sys.argv[1].decode('utf-8')
    output_dir = sys.argv[2]
    lyrics_path = op.join(output_dir, 'lyrics.txt')

    with codecs.open(lyrics_path, 'w', 'utf-8') as fp:
        for track in get_tracks(playlist_name):
            path = track.path
            output_path = op.join(output_dir, op.basename(path))
            shutil.copy(path, output_path)
            print '%s - %s' % (track.title, track.artist)

            fp.write('Title: %s\n' % track.title)
            fp.write('Artist: %s\n\n' % track.artist)
            fp.write(track.lyrics + '\n\n')
            fp.write('=' * 80 + '\n\n')


def get_tracks(playlist_name):
    import itunes
    tunes = itunes.ITunes()
    playlist = tunes[playlist_name]
    for track in playlist.tracks:
        yield track


if __name__ == '__main__':
    main()
