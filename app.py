from flask import Flask, render_template, request, send_from_directory, redirect, flash
import os
from pytube import YouTube
import instaloader

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Error messages ke liye

DOWNLOAD_FOLDER = os.path.join('static', 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']

    try:
        if 'youtube.com' in url or 'youtu.be' in url:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            output_path = stream.download(output_path=DOWNLOAD_FOLDER)
            filename = os.path.basename(output_path)
            return redirect(f'/download_file/{filename}')

        elif 'instagram.com' in url:
            loader = instaloader.Instaloader(dirname_pattern=DOWNLOAD_FOLDER)
            loader.download_post(instaloader.Post.from_shortcode(loader.context, url.split("/")[-2]), target="")
            flash("Instagram download done. Please check the server folder manually.")
            return redirect('/')

        else:
            flash("❌ Unsupported link. Please enter a valid YouTube or Instagram URL.")
            return redirect('/')

    except Exception as e:
        print(e)
        flash(f"⚠️ Error: {str(e)}")
        return redirect('/')

@app.route('/download_file/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
