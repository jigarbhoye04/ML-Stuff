import cmd
import json
import os
import threading
import time
import requests
import vlc
import yt_dlp
from ascii_magic import AsciiArt

class Song:
    def __init__(self, title, artist, youtube_id, thumbnail_url=None):
        self.title = title
        self.artist = artist
        self.youtube_id = youtube_id
        self.thumbnail_url = thumbnail_url

    def __str__(self):
        return f"{self.title} by {self.artist}"

class MusicCLI(cmd.Cmd):
    intro = "Welcome to MusicCLI! Here are the available commands:"
    prompt = "(MusicCLI) "

    def __init__(self):
        super().__init__()
        self.songs = []
        self.current_song = None
        self.player = vlc.Instance().media_player_new()
        self.load_data()
        self.display_commands()

    def display_commands(self):
        commands = [
            ("s <query>", "search", "Search for a song and play it"),
            ("p", "pause", "Pause or resume the current song"),
            ("x", "stop", "Stop the current song"),
            ("n", "next", "Play the next song"),
            ("l", "list", "List all songs"),
            ("play <number>", "play", "Play a specific song by number"),
            ("q", "quit", "Exit the program"),
            ("h", "help", "Show this help message")
        ]
        print("\nCommands:")
        for alias, cmd, desc in commands:
            print(f"  {alias:<15} {desc}")
        print()

    def load_data(self):
        if os.path.exists("songs.json"):
            with open("songs.json", "r") as f:
                song_data = json.load(f)
                self.songs = []
                for song in song_data:
                    # Handle potential missing thumbnail_url
                    if 'thumbnail_url' not in song:
                        song['thumbnail_url'] = None
                    self.songs.append(Song(**song))

    def save_data(self):
        with open("songs.json", "w") as f:
            json.dump([vars(song) for song in self.songs], f)

    def do_s(self, arg):
        "Search for a song and play it: s <query>"
        self.do_search(arg)

    def do_search(self, arg):
        "Search for a song and play it: search <query>"
        ydl_opts = {
            'default_search': 'ytsearch',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
                song = Song(info['title'], info['uploader'], info['id'], info['thumbnail'])
                self.songs.append(song)
                self.save_data()
                print(f"Found and playing: {song}")
                self.play_song(song)
            except Exception as e:
                print(f"An error occurred: {e}")

    def play_song(self, song):
        self.current_song = song
        url = f"https://www.youtube.com/watch?v={song.youtube_id}"
        media = self.player.get_instance().media_new(url)
        self.player.set_media(media)
        self.player.play()
        threading.Thread(target=self.display_now_playing, daemon=True).start()

    def display_now_playing(self):
        while self.player.is_playing():
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Now playing: {self.current_song}")
            if self.current_song.thumbnail_url:
                self.display_ascii_art(self.current_song.thumbnail_url)
            print("\nPress 'p' to pause/resume, 'x' to stop, 'n' for next song")
            time.sleep(1)

    def display_ascii_art(self, url):
        try:
            response = requests.get(url)
            with open("temp_thumbnail.jpg", "wb") as f:
                f.write(response.content)
            ascii_art = AsciiArt.from_image("temp_thumbnail.jpg")
            ascii_art.to_terminal(columns=60, width_ratio=2)
            os.remove("temp_thumbnail.jpg")
        except Exception as e:
            print(f"Couldn't display album art: {e}")

    def do_p(self, arg):
        "Pause or resume the current song"
        self.do_pause(arg)

    def do_pause(self, arg):
        "Pause or resume the current song"
        if self.player.is_playing():
            self.player.pause()
        else:
            self.player.play()
        self.display_commands()  # Display commands after pausing/resuming

    def do_x(self, arg):
        "Stop the current song"
        self.do_stop(arg)

    def do_stop(self, arg):
        "Stop the current song"
        self.player.stop()
        self.current_song = None
        self.display_commands()  # Display commands after stopping

    def do_n(self, arg):
        "Play the next song in the list"
        self.do_next(arg)

    def do_next(self, arg):
        "Play the next song in the list"
        if self.current_song:
            current_index = self.songs.index(self.current_song)
            next_index = (current_index + 1) % len(self.songs)
            self.play_song(self.songs[next_index])
        self.display_commands()  # Display commands after playing next song

    def do_l(self, arg):
        "List all songs"
        self.do_list(arg)

    def do_list(self, arg):
        "List all songs"
        for i, song in enumerate(self.songs, 1):
            print(f"{i}. {song}")
        self.display_commands()  # Display commands after listing songs

    def do_play(self, arg):
        "Play a specific song by number: play <song_number>"
        try:
            song = self.songs[int(arg) - 1]
            self.play_song(song)
        except (ValueError, IndexError):
            print("Invalid song number.")
        self.display_commands()  # Display commands after playing a specific song

    def do_q(self, arg):
        "Exit the program"
        return self.do_quit(arg)

    def do_quit(self, arg):
        "Exit the program"
        self.player.stop()
        print("Thank you for using MusicCLI!")
        return True

    def do_h(self, arg):
        "Show help message"
        self.do_help(arg)

    def do_help(self, arg):
        "Show help message"
        self.display_commands()

if __name__ == "__main__":
    MusicCLI().cmdloop()