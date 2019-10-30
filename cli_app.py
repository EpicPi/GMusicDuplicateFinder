from gmusicapi import Mobileclient
import json

client = Mobileclient()

oauth = raw_input("first time?")
if oauth == "y":
    client.perform_oauth()
else:
    # todo: store oauth data in non-default
    client.oauth_login(Mobileclient.FROM_MAC_ADDRESS)

playlists = client.get_all_user_playlist_contents()
songs = []

# todo: allow playlist selection
playlist = "Main"

for p in playlists:
    if p["name"] == playlist:
        for track in p["tracks"]:
            try:
                song = client.get_track_info(track["trackId"])
                song["entryId"] = track["id"]
                songs.append(song)
            except:
                print("Wasn't able to obtain information for one song")

# with open("data.txt", "w") as outfile:
#     json.dump(songs, outfile)

used = []


def isSimilar(song1, song2):
    s1 = song1["title"]
    s2 = song2["title"]
    return s1 in s2 or s2 in s1


similar = {}

print("starting now")
for i in range(len(songs)):
    if not songs[i] in used:
        for j in range(i+1, len(songs)):
            if not songs[j] in used:
                if isSimilar(songs[i], songs[j]):
                    used.append(songs[j])
                    if songs[i]["title"] not in similar:
                        similar[songs[i]["title"]] = [songs[i]]
                    similar[songs[i]["title"]].append(songs[j])


for sim in similar:
    print("---" + sim + "---")
    delete = True
    while delete:
        ss = similar[sim]
        for i in range(len(ss)):
            print(str(i) + " " + ss[i]["title"] + " by " + ss[i]["artist"])
        which = int(input("which one to delete? (if none then type n+1)"))
        if which >= len(ss):
            delete = False
        else:
            print(
                "deleted" + str(client.remove_entries_from_playlist(ss[which]["entryId"])))
            ss.pop(which)