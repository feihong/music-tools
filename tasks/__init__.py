from invoke import Collection
from . import main, copy, mp3, meta, search, convert


namespace = Collection.from_module(main)
for mod in (copy, mp3, meta, search, convert):
    namespace.add_collection(mod)
