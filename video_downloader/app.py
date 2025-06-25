from flask import Flask, render_template, request, send_from_directory
from pytube import YouTube
import instaloader
import os
import re

app = Flask(__name__)
DOWNLOAD_FOLDER = 'static/downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    video_url = ""
    if request.method == "POST":
        url = request.form.get("url")
        try:
            if "youtube.com" in url or "youtu.be" in url:
                yt = YouTube(url)
                stream = yt.streams.get_highest_resolution()
                output_path = stream.download(output_path=DOWNLOAD_FOLDER)
                video_url = f"/{output_path}"
                message = "YouTube video downloaded successfully!"
            elif "instagram.com" in url:
                loader = instaloader.Instaloader(dirname_pattern=DOWNLOAD_FOLDER, save_metadata=False)
                shortcode = re.search(r'/p/([A-Za-z0-9_\-]+)/?', url)
                if shortcode:
                    loader.download_post(instaloader.Post.from_shortcode(loader.context, shortcode.group(1)), target="")
                    message = "Instagram post downloaded. Check static/downloads folder."
                else:
                    message = "Invalid Instagram URL format."
            else:
                message = "Unsupported URL!"
        except Exception as e:
            message = f"Error: {str(e)}"

    return render_template("index.html", message=message, video_url=video_url)

if __name__ == "__main__":
    app.run(debug=True)
