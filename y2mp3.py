# Youtube Playlist to MP4 and MP3 downloader
# Author : Arul Benjamin Chandru E

# Authored on : 18-May-2024
# This hobby project extracts the Youtube video playlist into MP4 and then converts into MP3
# Output will be saved in given output folder path

import os
import threading
from math import ceil
from pytube import YouTube, Playlist
from moviepy.editor import VideoFileClip
import streamlit as st

def download_videos(playlist_url, output_folder):
    """
    Download all videos from a YouTube playlist and extract audio as MP3 files.
    
    Args:
        playlist_url (str): URL of the YouTube playlist.
        output_folder (str): Path to the folder where MP3 files will be saved.
    """
    try:
        # Load the playlist
        p = Playlist(playlist_url)
        # Filter out private or unavailable videos
        links = [video_url for video_url in p.video_urls if 'private' not in video_url]
    except Exception as e:
        st.error(f"Error loading playlist: {e}")
        return

    # Display playlist information
    st.write(f"Playlist Name : {p.title}")
    st.write(f"Channel Name  : {p.owner}")
    st.write(f"Total Videos  : {p.length}")
    st.write(f"Total Views   : {p.views}")

    # Get list of video URLs from the playlist
    size = ceil(len(links) / 4)  # Split links into chunks for multithreading
    link_chunks = [links[i:i+size] for i in range(0, len(links), size)]

    def downloader(link_chunk, thread_name):
        """
        Download videos and extract audio in a given chunk of links.
        
        Args:
            link_chunk (list): List of video URLs to download.
            thread_name (str): Name of the thread for logging purposes.
        """
        for url in link_chunk:
            try:
                yt = YouTube(url)  # Initialize YouTube object
                ys = yt.streams.get_highest_resolution()  # Get highest resolution stream
                filename = ys.download(output_folder)  # Download the video
                st.write(f"{thread_name} --> {filename.split('/')[-1]} Downloaded")
                extract_audio(filename, output_folder)  # Extract audio
                os.remove(filename)  # Delete the video file
                st.write(f"{thread_name} --> {filename.split('/')[-1]} Deleted")
            except Exception as e:
                st.error(f"Failed to download {url}: {e}")

    # Create and start threads for downloading videos
    threads = []
    for i, chunk in enumerate(link_chunks):
        t = threading.Thread(target=downloader, args=(chunk, f'threading {i+1}'), name=f'd{i+1}')
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

def extract_audio(video_file_path, output_folder):
    """
    Extract audio from a video file and save it as an MP3 file.
    
    Args:
        video_file_path (str): Path to the video file.
        output_folder (str): Path to the folder where MP3 file will be saved.
    """
    try:
        video = VideoFileClip(video_file_path)  # Load the video file
        audio = video.audio  # Extract audio from video
        audio_file_path = os.path.join(output_folder, os.path.splitext(os.path.basename(video_file_path))[0] + ".mp3")
        audio.write_audiofile(audio_file_path)  # Save audio as MP3 file
        st.write(f"Audio extracted successfully for {video_file_path}")
    except Exception as e:
        st.error(f"An error occurred while extracting audio from {video_file_path}: {e}")

# Streamlit UI
st.title("YouTube Playlist to MP3 Converter")

# Input fields for playlist URL and output folder
playlist_url = st.text_input("Enter Playlist URL:")
output_folder = st.text_input("Enter Output Folder Path:")

# Button to start the download and extraction process
if st.button("Download and Extract Audio"):
    if playlist_url and output_folder:
        download_videos(playlist_url, output_folder)
    else:
        st.error("Please provide both Playlist URL and Output Folder Path.")
