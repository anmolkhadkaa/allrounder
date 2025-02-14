import os
import subprocess
import sys
import json
from yt_dlp import YoutubeDL
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
import requests
from io import BytesIO

# Required Python packages
required_packages = ["yt-dlp", "mutagen"]

# Install missing packages if necessary
def install_packages(packages):
    installed_packages = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True).stdout
    for package in packages:
        if package not in installed_packages:
            print(f"📦 Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_packages(required_packages)

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except FileNotFoundError:
        return False

if not check_ffmpeg():
    print("❌ FFmpeg is not installed! Please install it manually.")
    sys.exit(1)

def download_audio(video_urls, save_path, bitrate):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(save_path, '%(title)s - Anmol Khadka.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': bitrate
        }],
        'postprocessor_args': ['-metadata', 'artist=Anmol Khadka'],
        'merge_output_format': 'mp3',
        'writethumbnail': True  # Automatically download the thumbnail as well
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_urls[0], download=True)  # Extract video info
        file_name = ydl.prepare_filename(info_dict)  # Get the file name of the audio
        thumbnail_url = info_dict.get('thumbnail', None)  # Get thumbnail URL

        ydl.download(video_urls)
        print("🎵 Audio download complete!")

        # If thumbnail exists, directly embed it into the MP3 file
        if thumbnail_url:
            response = requests.get(thumbnail_url)
            audio_file = MP3(file_name, ID3=ID3)
            audio_file.tags.add(
                APIC(
                    encoding=3,  # UTF-8
                    mime='image/jpeg',
                    type=3,  # Album art
                    desc='Cover',
                    data=response.content
                )
            )
            audio_file.save()
            print("🎵 Thumbnail added to MP3 file!")

def download_video(video_urls, save_path):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': os.path.join(save_path, '%(title)s - Anmol Khadka.%(ext)s'),
        'merge_output_format': 'mp4'
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_urls)
    print("🎬 Video download complete!")

def download_playlist(video_urls, save_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(save_path, '%(playlist)s/%(title)s - Anmol Khadka.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320'
        }],
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_urls)
    print("📂 Playlist downloaded successfully!")

def download_tiktok(video_urls, save_path):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(save_path, '%(title)s - Anmol Khadka.%(ext)s'),
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegMetadata',
        }]
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_urls)
    print("🎬 TikTok video download complete!")

def download_instagram(video_urls, save_path):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(save_path, '%(title)s - Anmol Khadka.%(ext)s'),
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegMetadata',
        }]
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_urls)
    print("🎬 Instagram video download complete!")

def download_facebook(video_urls, save_path):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(save_path, '%(title)s - Anmol Khadka.%(ext)s'),
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegMetadata',
        }]
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_urls)
    print("🎬 Facebook video download complete!")

def convert_video_to_audio(video_file):
    audio_file = video_file.rsplit(".", 1)[0] + " - Anmol Khadka.mp3"
    subprocess.run(["ffmpeg", "-i", video_file, "-q:a", "0", "-map", "a", audio_file])
    print(f"🎵 Converted {video_file} to MP3!")

print("\n🎵 Multi-Platform Downloader 🎥 by Anmol Khadka")
print("[1] Download Audio (MP3 with Cover Art)")
print("[2] Download Video (MP4 in all qualities)")
print("[3] Download Playlist")
print("[4] Convert Downloaded Video to MP3")
print("[5] Download TikTok Video")
print("[6] Download Instagram Video")
print("[7] Download Facebook Video")

choice = input("Enter your choice (1/2/3/4/5/6/7): ")

if choice in ["1", "2", "3"]:
    urls = input("📌 Enter video URL(s) (comma-separated): ").split(",")
    video_urls = [url.strip() for url in urls]
    save_path = input("💾 Enter save path (default: ~/Downloads): ") or os.path.expanduser("~/Downloads")
    
    if choice == "1":
        bitrate = input("🎵 Choose bitrate (128, 192, 320 kbps) [Default: 320]: ") or "320"
        download_audio(video_urls, save_path, bitrate)
    elif choice == "2":
        download_video(video_urls, save_path)
    elif choice == "3":
        download_playlist(video_urls, save_path)

elif choice == "4":
    video_file = input("📁 Enter video file path to convert: ")
    convert_video_to_audio(video_file)
elif choice == "5":
    urls = input("📌 Enter TikTok video URL(s) (comma-separated): ").split(",")
    video_urls = [url.strip() for url in urls]
    save_path = input("💾 Enter save path (default: ~/Downloads): ") or os.path.expanduser("~/Downloads")
    download_tiktok(video_urls, save_path)
elif choice == "6":
    urls = input("📌 Enter Instagram video URL(s) (comma-separated): ").split(",")
    video_urls = [url.strip() for url in urls]
    save_path = input("💾 Enter save path (default: ~/Downloads): ") or os.path.expanduser("~/Downloads")
    download_instagram(video_urls, save_path)
elif choice == "7":
    urls = input("📌 Enter Facebook video URL(s) (comma-separated): ").split(",")
    video_urls = [url.strip() for url in urls]
    save_path = input("💾 Enter save path (default: ~/Downloads): ") or os.path.expanduser("~/Downloads")
    download_facebook(video_urls, save_path)
else:
    print("❌ Invalid choice. Please restart and select 1, 2, 3, 4, 5, 6, or 7.")
