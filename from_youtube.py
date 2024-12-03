import os
from yt_dlp import YoutubeDL

def download_youtube_channel(channel_url, output_folder="downloads", cookies_file=None, playlists=None):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # yt-dlp options
    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",  # Download highest quality video+audio
        "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),  # Save videos in the specified folder
        "writesubtitles": True,  # Attempt to download subtitles
        "subtitleslangs": ["en"],  # Download English subtitles and all available ones
        "writeautomaticsub": True,  # Also download auto-generated subtitles
        "subtitlesformat": "srt",  # Save subtitles in SRT format
        "writeinfojson": True,  # Save metadata in JSON format
        "writeannotations": True,  # Include annotations (if applicable)
        "writethumbnail": True,  # Download video thumbnails
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",  # Convert videos to MP4 format
            },
            # Add subtitle post-processor
            {
                'key': 'FFmpegSubtitlesConvertor',
                'format': 'srt',
            },
        ],
        "merge_output_format": "mp4",  # Ensure merged files are in MP4
        # Skip downloading subtitles if an error occurs
        "ignoreerrors": True,  
        # Skip downloading videos that already exist
        "nooverwrites": True,
    }

    # Add cookies file if provided
    if cookies_file and os.path.exists(cookies_file):
        ydl_opts["cookiefile"] = cookies_file

    # Download the videos and metadata
    with YoutubeDL(ydl_opts) as ydl:
        try:
            if playlists:
                # Download specific playlists
                for playlist_url in playlists:
                    print(f"Downloading playlist: {playlist_url}")
                    ydl.download([playlist_url])
            else:
                # Download entire channel
                ydl.download([channel_url])
        except Exception as e:
            print(f"Error downloading {channel_url}: {e}")



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
        playlists = channel.get('playlists', None)  # Get playlists if specified
        
        # Create channel-specific output folder
        output_folder = os.path.join("youtube_channel_downloads", channel_name)
        
        print(f"Downloading channel: {channel_name}")
        download_youtube_channel(channel_url, output_folder, cookies_file, playlists)
    
