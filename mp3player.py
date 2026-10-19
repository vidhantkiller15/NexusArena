"""
Standalone music helpers for Nexus Performante Arena.
Used by core.music — also runnable as a simple CLI.

Backends:
  • Local files → pygame
  • YouTube / online → yt-dlp stream URL + VLC
"""
from __future__ import annotations

import os
import re
from typing import Any, Optional, Tuple

# Lazy heavy imports so importing this module is cheap


def play_local(file: str):
    """Blocking play of a local audio file (VLC preferred, pygame fallback)."""
    path = os.path.abspath(file)
    if not os.path.isfile(path):
        print("File not found:", file)
        return

    # Prefer VLC
    try:
        from pathlib import Path as _P
        player = make_vlc_player(_P(path).as_uri())
        print("Playing:", os.path.basename(path), "(VLC)")
        player.play()
        import time
        while True:
            st = player.get_state()
            try:
                code = int(st)
            except Exception:
                try:
                    code = int(st.value)
                except Exception:
                    code = -1
                    name = str(st).lower()
                    if "ended" in name or "stopped" in name or "error" in name:
                        code = 6
            if code in (5, 6, 7):
                break
            time.sleep(0.2)
        player.stop()
        return
    except Exception:
        pass

    try:
        import pygame
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        print("Playing:", os.path.basename(path), "(pygame)")
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print("Play failed:", e)
        print("Install VLC media player +:  pip install python-vlc")


def find_song(song_name: str, folder: str = "C:\\") -> Optional[str]:
    """Walk a folder tree looking for an audio file matching song_name."""
    exts = (".mp3", ".wav", ".ogg", ".flac", ".m4a")
    needle = (song_name or "").lower().strip()
    if not needle:
        return None
    # Prefer user music folders first if scanning whole drive would be huge
    roots = []
    if folder and folder not in (".", ""):
        roots.append(folder)
    music = os.path.expandvars(r"%USERPROFILE%\Music")
    desktop = os.path.expandvars(r"%USERPROFILE%\Desktop")
    downloads = os.path.expandvars(r"%USERPROFILE%\Downloads")
    for r in (music, desktop, downloads):
        if r not in roots and os.path.isdir(r):
            roots.insert(0, r)

    for root_dir in roots:
        try:
            for root, _dirs, files in os.walk(root_dir):
                # skip heavy system dirs
                low = root.lower()
                if any(
                    x in low
                    for x in (
                        "\\windows\\",
                        "\\$recycle",
                        "\\appdata\\local\\temp",
                        "\\node_modules",
                    )
                ):
                    continue
                for file in files:
                    if needle in file.lower() and file.lower().endswith(exts):
                        return os.path.join(root, file)
        except Exception:
            continue
    return None


def resolve_online(query: str) -> Tuple[str, str]:
    """
    Resolve a song name or URL to (stream_url, title) via yt-dlp.
    Does not download the full file.
    """
    from yt_dlp import YoutubeDL

    q = (query or "").strip()
    if not q:
        raise ValueError("Empty query")

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "socket_timeout": 25,
    }

    is_url = bool(
        re.search(r"https?://", q, re.I)
        or "youtube.com" in q
        or "youtu.be" in q
    )
    if q.startswith("ytsearch"):
        search = q
    elif is_url:
        search = q
    else:
        search = f"ytsearch1:{q}"

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search, download=False)
        if not info:
            raise RuntimeError("No results")
        if "entries" in info:
            entries = [e for e in (info.get("entries") or []) if e]
            if not entries:
                raise RuntimeError("No results")
            info = entries[0]
        # Prefer direct streamable URL from formats
        url = info.get("url")
        if not url:
            # re-extract with format if needed
            webpage = info.get("webpage_url") or info.get("original_url") or search
            info2 = ydl.extract_info(webpage, download=False)
            if info2 and "entries" in info2:
                ents = [e for e in (info2.get("entries") or []) if e]
                info2 = ents[0] if ents else info2
            info = info2 or info
            url = (info or {}).get("url")
        title = (info or {}).get("title") or q
        if not url:
            raise RuntimeError("No stream URL")
        return str(url), str(title)


def make_vlc_player(stream_url: str) -> Any:
    """Create a VLC media player for a stream or file URL."""
    import vlc

    instance = vlc.Instance("--no-video", "--quiet")
    player = instance.media_player_new()
    media = instance.media_new(stream_url)
    player.set_media(media)
    return player


def play_online(query: str) -> None:
    """Blocking online play (CLI). Press Enter to stop."""
    url, title = resolve_online(query)
    player = make_vlc_player(url)
    print("Now Playing:", title)
    player.play()
    input("Press ENTER to stop...")
    player.stop()


def main() -> None:
    print("\n1. Play file")
    print("2. Search PC")
    print("3. Song name (YouTube)")
    print("4. YouTube link")
    print("5. Exit")

    while True:
        choice = input("\nChoice: ").strip()
        if choice == "1":
            path = input("File path: ").strip()
            if path:
                play_local(path)
        elif choice == "2":
            name = input("Song name: ").strip()
            song = find_song(name)
            if song:
                play_local(song)
            else:
                print("Not found.")
        elif choice == "3":
            name = input("Song name: ").strip()
            if name:
                play_online(name)
        elif choice == "4":
            url = input("YouTube URL: ").strip()
            if url:
                play_online(url)
        elif choice == "5":
            break


if __name__ == "__main__":
    main()
