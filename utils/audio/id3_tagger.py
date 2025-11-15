#!/usr/bin/env python3
"""
ID3 Tagger for Pensieri in codice podcast episodes
Adds ID3v2 tags to MP3 files that are missing them
"""

import os
import sys
import argparse
from pathlib import Path
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TPE2, COMM, APIC
from mutagen.mp3 import MP3

# Fixed metadata values
ARTIST = "Valerio Galano"
ALBUM = "Pensieri in codice"
ALBUM_ARTIST = "Valerio Galano"
GENRE = "Technology"
COMMENT = "Il podcast dove si ragiona da informatici"


def has_id3_tags(file_path):
    """Check if MP3 file has ID3v2 tags"""
    try:
        audio = MP3(file_path)
        # Check if there are any ID3 tags
        return len(audio.tags) > 0 if audio.tags else False
    except Exception:
        return False


def add_id3_tags(file_path, cover_path=None):
    """Add ID3v2 tags to MP3 file"""
    try:
        # Try to load existing tags or create new ones
        try:
            audio = ID3(file_path)
        except:
            audio = ID3()

        # Extract episode number from filename (e.g., PIC123.mp3 -> 123)
        filename = Path(file_path).stem
        episode_num = ''.join(filter(str.isdigit, filename))
        title = f"Episodio {episode_num}" if episode_num else filename

        # Add basic tags
        audio.add(TIT2(encoding=3, text=title))  # Title
        audio.add(TPE1(encoding=3, text=ARTIST))  # Artist
        audio.add(TALB(encoding=3, text=ALBUM))  # Album
        audio.add(TPE2(encoding=3, text=ALBUM_ARTIST))  # Album Artist
        audio.add(TCON(encoding=3, text=GENRE))  # Genre
        audio.add(COMM(encoding=3, lang='ita', desc='Comment', text=COMMENT))  # Comment

        # Add cover art if available
        if cover_path and os.path.exists(cover_path):
            with open(cover_path, 'rb') as cover_file:
                audio.add(
                    APIC(
                        encoding=3,
                        mime='image/png',
                        type=3,  # Cover (front)
                        desc='Cover',
                        data=cover_file.read()
                    )
                )

        # Save tags to file
        audio.save(file_path, v2_version=3)
        return True
    except Exception as e:
        print(f"Error adding tags to {file_path}: {e}", file=sys.stderr)
        return False


def process_directory(audio_dir, cover_path=None):
    """Process all MP3 files in directory"""
    audio_dir = Path(audio_dir)

    if not audio_dir.exists():
        print(f"Error: Directory {audio_dir} does not exist", file=sys.stderr)
        return 1

    mp3_files = list(audio_dir.glob("*.mp3"))

    if not mp3_files:
        print(f"No MP3 files found in {audio_dir}")
        return 0

    processed = 0
    skipped = 0
    failed = 0

    for mp3_file in mp3_files:
        if has_id3_tags(mp3_file):
            print(f"Skipping {mp3_file.name} (already has ID3 tags)")
            skipped += 1
            continue

        print(f"Adding ID3 tags to {mp3_file.name}...")
        if add_id3_tags(mp3_file, cover_path):
            processed += 1
        else:
            failed += 1

    print(f"\nSummary:")
    print(f"  Processed: {processed}")
    print(f"  Skipped: {skipped}")
    print(f"  Failed: {failed}")

    return 0 if failed == 0 else 1


def main():
    parser = argparse.ArgumentParser(
        description='Add ID3v2 tags to podcast MP3 files'
    )
    parser.add_argument(
        '--audio_dir',
        required=True,
        help='Directory containing MP3 files'
    )
    parser.add_argument(
        '--cover',
        help='Path to cover image (optional)'
    )

    args = parser.parse_args()

    return process_directory(args.audio_dir, args.cover)


if __name__ == '__main__':
    sys.exit(main())
