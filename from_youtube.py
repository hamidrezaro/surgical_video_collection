import os
from yt_dlp import YoutubeDL

def download_youtube_channel(channel_url, output_folder="downloads", cookies_file=None):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # yt-dlp options
    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",  # Download highest quality video+audio
        "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),  # Save videos in the specified folder
        "writesubtitles": True,  # Download subtitles if available
        "subtitleslangs": ["en"],  # Download English subtitles and all available ones
        "writeinfojson": True,  # Save metadata in JSON format
        "writeannotations": True,  # Include annotations (if applicable)
        "writethumbnail": True,  # Download video thumbnails
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",  # Convert videos to MP4 format
            }
        ],
        "merge_output_format": "mp4",  # Ensure merged files are in MP4
    }

    # Add cookies file if provided
    if cookies_file and os.path.exists(cookies_file):
        ydl_opts["cookiefile"] = cookies_file

    # Download the videos and metadata
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([channel_url])



if __name__ == "__main__":

    import json
    
    # Load channels from config file
    with open('yt_channels.json', 'r') as f:
        channels = json.load(f)
    
    # Path to cookies file (you'll need to export this from your browser)
    cookies_file = "youtube_cookies.txt"
    
    # Process each channel
    for channel in channels:
        channel_name = channel['name']
        channel_url = channel['url']
        
        # Create channel-specific output folder
        output_folder = os.path.join("youtube_channel_downloads", channel_name)
        
        print(f"Downloading channel: {channel_name}")
        download_youtube_channel(channel_url, output_folder, cookies_file)
    
