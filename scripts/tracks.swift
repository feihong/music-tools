// https://developer.apple.com/documentation/ituneslibrary

import iTunesLibrary

guard let library = try? ITLibrary(apiVersion: "1.1") else {
  print("Cannot load ITLibrary")
  exit(1)
}

let playlists = library.allPlaylists

func getMusicPlaylist() -> ITLibPlaylist? {
  for playlist in playlists {
    if playlist.distinguishedKind == .kindMusic {
      return playlist
    }
  }
  return nil
}

guard let playlist = getMusicPlaylist() else {
  print("Please enter name of playlist you want to search for")
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
