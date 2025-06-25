from flask import Flask, render_template, request, send_file, redirect, flash
from pytube import YouTube
import os
import uuid
import instaloader

app = Flask(__name__)
app.secret_key = 'anish_youtube_insta_key'  # Replaceable but required

DOWNLOAD_FOLDER = "static/downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get("url")
    if not url:
        flash("Please enter a URL.")
        return redirect('/')

    try:
        filename = f"{uuid.uuid4()}.mp4"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        if "youtube.com" in url or "youtu.be" in url:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)
            return send_file(filepath, as_attachment=True)

        elif "instagram.com" in url:
            shortcode = url.strip("/").split("/")[-1]
            loader = instaloader.Instaloader(dirname_pattern=DOWNLOAD_FOLDER, save_metadata=False)
            loader.download_post(instaloader.Post.from_shortcode(loader.context, shortcode), target="post")
            
            # Get downloaded file (first .mp4 found)
            for file in os.listdir(DOWNLOAD_FOLDER):
                if file.endswith(".mp4"):
                    return send_file(os.path.join(DOWNLOAD_FOLDER, file), as_attachment=True)

            flash("Instagram video not found or unsupported.")
            return redirect('/')

        else:
            flash("Only YouTube or Instagram URLs are supported.")
            return redirect('/')

    except Exception as e:
        flash(f"Error: {str(e)}")
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
