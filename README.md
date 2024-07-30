# MusicCLI Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Features](#features)
5. [Commands](#commands)
6. [Troubleshooting](#troubleshooting)

## Introduction

MusicCLI is a command-line interface (CLI) application that allows you to search for, play, and manage music directly from your terminal. It features a simple and intuitive interface, with the ability to display ASCII art album covers and control playback without leaving the command line.

## Installation

### Prerequisites

- Python 3.7 or higher
- VLC media player

### Steps

1. Clone the repository or download the `music_cli.py` file.

2. Install the required Python packages:

   ```
   pip install python-vlc yt-dlp requests ascii-magic
   ```

3. Ensure VLC media player is installed on your system. You can download it from the [official VLC website](https://www.videolan.org/vlc/).

## Getting Started

1. Open a terminal or command prompt.

2. Navigate to the directory containing `music_cli.py`.

3. Run the script:

   ```
   python music_cli.py
   ```

4. You should see the welcome message, available commands, and the MusicCLI prompt:

   ```
   Welcome to MusicCLI! Here are the available commands:

   Commands:
     s <query>        Search for a song and play it
     p                Pause or resume the current song
     x                Stop the current song
     n                Play the next song
     l                List all songs
     play <number>    Play a specific song by number
     q                Exit the program
     h                Show this help message

   (MusicCLI)
   ```

## Features

- Search for songs on YouTube and play them instantly
- Display ASCII art album covers
- Control playback (play, pause, stop, next)
- Manage a local library of songs
- Interactive "Now Playing" display
- Command aliases for quick access
- Display of all available commands on startup

## Commands

Here's a list of available commands in MusicCLI:

### `s <query>` or `search <query>`
Search for a song and play it immediately.
Example: `s Shape of You Ed Sheeran`

### `p` or `pause`
Pause or resume the current song.

### `x` or `stop`
Stop the current song.

### `n` or `next`
Play the next song in the list.

### `l` or `list`
Display all songs in your library.

### `play <song_number>`
Play a specific song from your library by its number.
Example: `play 1`

### `q` or `quit`
Exit the program.

### `h` or `help`
Display a list of available commands.

## Troubleshooting

1. **VLC not found**: Ensure VLC is installed and its path is added to your system's PATH environment variable.

2. **Playback issues**: Make sure you have a stable internet connection, as the app streams music from YouTube.

3. **ASCII art not displaying**: Check if your terminal supports ASCII art display. Try adjusting your terminal window size if the art appears distorted.

4. **Song search fails**: Verify your internet connection and try again. If the problem persists, the song might not be available on YouTube.

For any other issues or feature requests, please open an issue on the project's GitHub repository.

---

We hope you enjoy using MusicCLI! For more information or to contribute to the project, please visit our GitHub repository.