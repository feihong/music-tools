/*
Extract track metadata of all music tracks to tracks.json

This script is much, much faster than the Python equivalent that uses PyObjC.

Links:
https://developer.apple.com/documentation/ituneslibrary
https://developer.apple.com/documentation/ituneslibrary/itlibmediaitem
*/
import Foundation
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
  print("Failed to access music playlist")
  exit(1)
}

let dateFormatter = DateFormatter()
dateFormatter.dateFormat = "yyyy-MM-dd"

extension Date {
  func getFormattedDate(formatter: DateFormatter) -> String {
    return formatter.string(from: self)
  }
}

let dictArray = playlist.items.map { track in
  [
    "title": track.title,
    "artist": track.artist?.name ?? "",
    "album": track.album.title ?? "",
    "rating": track.rating / 20,
    "genre": track.genre,
    "comments": track.comments ?? "",
    "location": track.location!.path,
    "added": track.addedDate?.getFormattedDate(formatter: dateFormatter) ?? "",
  ]
}

let jsonData = try! JSONSerialization.data(withJSONObject: dictArray, options: .prettyPrinted)

let directoryUrl = URL(fileURLWithPath: FileManager.default.currentDirectoryPath, isDirectory: true)
let outputUrl = directoryUrl.appendingPathComponent("tracks.json")

try! jsonData.write(to: outputUrl)
