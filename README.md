# YT Video & Audio Downloader

## Overview
This project is a YouTube video and audio downloader that allows users to download videos in various resolutions or extract audio in multiple bitrates. It utilizes `yt-dlp` for robust video/audio extraction and `pytube` for additional YouTube functionalities. The downloader also displays the video's thumbnail before initiating the download.

## Features
- Fetches video details (title, duration, thumbnail, etc.).
- Provides resolution and bitrate selection for downloading.
- Supports downloading audio-only files in MP3 format.
- Displays a progress bar during downloads.
- Saves downloads to a user-specified directory.

## Requirements
Ensure you have Python installed (preferably Python 3.9 or newer). Install dependencies using:

```sh
pip install -r requirements.txt
```

### Dependencies
- `pytube` – Fetching video metadata.
- `yt-dlp` – Extracting and downloading video/audio.
- `pillow` – Handling and displaying thumbnails.
- `requests` – Making HTTP requests.
- `tqdm` – Displaying download progress.


### Steps:
1. Provide a YouTube video URL.
2. Select the desired download directory.
3. Choose between video or audio download.
4. Pick the resolution or bitrate.
5. Wait for the download to complete.

## Example Output
```
Enter the desired download directory:
1) Custom path
2) Downloads

Saving to /Users/YourName/Downloads
Which Type do you want to download?
1) Video
2) Audio

Resolutions Available:
1. 1080p
2. 720p
3. 480p
Enter Resolution Index:

Downloading...
Download complete! Saved in /Users/YourName/Downloads
```

## Contributing
Feel free to fork this repository and submit pull requests with improvements or bug fixes.

## License
This project is open-source and available under the [MIT License](LICENSE).

