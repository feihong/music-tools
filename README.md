# Music Tools

A collection of (mostly Python) scripts to do stuff with your music collection.

# Installation

    pip install --user --requirement requirements.txt

# Commands

Export all tracks to tracks.json

    swift scripts/tracks_json.swift

Generate new JSON files containing tracks rated 2 stars and below

    jq 'map(select(.rating <= 2))' tracks.json > tracks-2-stars.json
