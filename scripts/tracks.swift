// https://developer.apple.com/documentation/ituneslibrary

import iTunesLibrary

guard let library = try? ITLibrary(apiVersion: "1.1") else {
  print("Cannot load ITLibrary")
  exit(1)
}

let playlists = library.allPlaylists

func getPlaylist(by: (ITLibPlaylist) -> Bool) -> ITLibPlaylist? {
  for playlist in playlists {
    if by(playlist) {
      return playlist
    }
  }
  return nil
}

func getMusicPlaylist() -> ITLibPlaylist? {
  return getPlaylist(by: {$0.distinguishedKind == .kindMusic})
}

func getPlaylist(name: String) -> ITLibPlaylist? {
  return getPlaylist(by: {$0.name == name})
}

let playlist = CommandLine.arguments.count <= 1 ? getMusicPlaylist() : getPlaylist(name: CommandLine.arguments[1])

guard let playlist = playlist else {
  print("Could not access the desired playlist")
  exit(1)
}

for track in playlist.items {
  print(track.title)
  print(track.artist?.name ?? "")
  print(track.location!.path)
  print(track.addedDate!)
  print(track.modifiedDate!)
  print()
}

print("Found \(playlist.items.count) music tracks")
