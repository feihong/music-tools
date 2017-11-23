from invoke import Collection
from . import main, copy, mp3, meta


namespace = Collection.from_module(main)
for mod in (copy, mp3, meta):
    namespace.add_collection(mod)
