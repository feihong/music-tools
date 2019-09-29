from invoke import Collection
from . import main, copy, mp3, meta, search


namespace = Collection.from_module(main)
for mod in (copy, mp3, meta, search):
    namespace.add_collection(mod)
