from invoke import Collection
from . import main, copy, mp3


namespace = Collection.from_module(main)
for mod in (copy, mp3):
    namespace.add_collection(mod)
