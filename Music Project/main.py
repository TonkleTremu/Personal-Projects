import json, winsound, time

FILEPATH = "Music Project/test_song.json"
SOUNDS_FILEPATH = "Music Project/sounds/"

song = {}

with open(FILEPATH) as raw_track:
    track = json.load(raw_track)
    print(track)
    for sound in track.values():
        winsound.PlaySound(SOUNDS_FILEPATH + sound["file"], winsound.SND_FILENAME)