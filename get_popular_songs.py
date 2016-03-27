"""
List songs rated 4 stars or above, grouped by artist.

"""
import itunes
from collections import defaultdict


def print_(s):
    if isinstance(s, unicode):
        print s.encode('utf-8')
    else:
        print s


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