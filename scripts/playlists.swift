/*:
https://developer.apple.com/documentation/ituneslibrary

Print all music playlists. If a playlist name is provided, print all tracks in that playlist.
*/

import iTunesLibrary

guard let library = try? ITLibrary(apiVersion: "1.1") else {
  print("Cannot load ITLibrary")
  exit(1)
}

let playlists = library.allPlaylists
let args = CommandLine.arguments

if let playlistName = args.count > 1 ? args[1].lowercased() : nil {
  let matches = playlists.filter { $0.name.lowercased() == playlistName }
  if matches.count == 0 {
    print("No playlists with that name")
  } else {
    for track in matches[0].items {
      print("\(track.title) by \(track.artist?.name ?? "")")
    }
  }
} else {
  for playlist in playlists {
    print("\(playlist.name) (\(playlist.items.count) items)")
  }
}
