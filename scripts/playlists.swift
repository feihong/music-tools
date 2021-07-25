// https://developer.apple.com/documentation/ituneslibrary

import iTunesLibrary

guard let library = try? ITLibrary(apiVersion: "1.1") else {
  print("Cannot load ITLibrary")
  exit(1)
}

let playlists = library.allPlaylists

for playlist in playlists {
  print("\(playlist.name) (\(playlist.items.count) items)")
}
