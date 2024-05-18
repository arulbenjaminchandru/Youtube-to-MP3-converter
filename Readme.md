# YouTube Playlist to MP3 Converter

This Python application downloads videos from a YouTube playlist, extracts audio from each video, saves the audio as MP3 files, and deletes the original video files. The application provides a simple web interface using Streamlit.

## Features

- Download all videos from a given YouTube playlist URL.
- Extract audio from each downloaded video and save as an MP3 file.
- Delete the original video files after audio extraction.
- Simple web interface for inputting playlist URL and output folder path.

## Requirements

- Python 3.x
- Required Python packages (listed in `requirements.txt`)

## Installation

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Install the required packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit application:

    ```bash
    streamlit y2mp3.py
    ```

2. Open the provided local URL in your web browser.
3. Enter the YouTube playlist URL and the output folder path.
4. Click the "Download and Extract Audio" button to start the process.

## License

This project is licensed under the MIT License.
