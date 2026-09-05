song_list = [
    {"id": 1, "name": "Song A", "duration": 160},
    {"id": 2, "name": "Song B", "duration": 200},
    {"id": 3, "name": "Song C", "duration": 180}
]

class PlayList:
    def add_song(self, name, duration):
        if not isinstance(duration, (int, float)):
            raise ValueError("Продолжительность песни должна быть числом.")
        
        if duration <= 0:
            raise ValueError("Продолжительность песни должна быть положительным числом.")
        
        if not isinstance(name, str):
            raise ValueError("Название песни должно быть строкой.")
        
        song_list.append({"id": len(song_list) + 1, "name": name, "duration": duration})

    def remove_song(self, song):
        if song in song_list:
            song_list.remove(song)
        else:
            raise ValueError("Песня не найдена в плейлисте.")

    def total_duration(self):
        total_duration = 0
        for song in song_list:
            total_duration += song["duration"]
        return total_duration

    def len_playlist(self):
        return len(song_list)

    def show_playlist(self):
        return song_list


playlist = PlayList()
playlist.add_song("Song D", 200)
playlist.remove_song({"id": 2, "name": "Song B", "duration": 200})
print(playlist.total_duration())
print(playlist.len_playlist())
print(playlist.show_playlist())