class Playlist:
    def __init__(self):
        self.songs = []

    def __len__(self):
        return len(self.songs)

    def add_song(self, name, duration):
        if not isinstance(duration, (int, float)):
            raise ValueError("Продолжительность песни должна быть числом.")
        
        if duration <= 0:
            raise ValueError("Продолжительность песни должна быть положительным числом.")
        
        if not isinstance(name, str):
            raise ValueError("Название песни должно быть строкой.")
        
        self.songs.append({"id": len(self.songs) + 1, "name": name, "duration": duration})

    def remove_song(self, name):
        for song in self.songs:
            if song["name"] == name:
                self.songs.remove(song)
                return

        print('Песня не найдена')  

    def total_duration(self):
        total_duration = 0
        for song in self.songs:
            total_duration += song["duration"]
        return total_duration

    def show_playlist(self):
        return self.songs


playlist = Playlist()

playlist.add_song("Song A", 100)
playlist.add_song("Song B", 200)
playlist.add_song("Song C", 300)

print('До изменения плейлиста:')
print(playlist.show_playlist())
print(playlist.total_duration())
print(len(playlist))


playlist.remove_song("Song B")
playlist.remove_song("Song X")

print('После изменения плейлиста:')
print(playlist.show_playlist())
print(playlist.total_duration())
print(len(playlist))

empty_playlist = Playlist()
print('Пустой плейлист:')
print(empty_playlist.show_playlist())