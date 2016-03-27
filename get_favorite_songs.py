"""
List songs rated 5 stars, grouped by genre.

"""

import itunes
from collections import defaultdict


def print_(s):
    """
    When printing to stdout, you need to encode to utf-8 or else you won't be
    able to redirect to a file.

    """
    if isinstance(s, unicode):
        print s.encode('utf-8')
    else:
        print s


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
