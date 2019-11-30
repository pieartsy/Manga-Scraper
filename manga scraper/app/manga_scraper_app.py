from flask import Flask
app = Flask(__name__)

@app.route('/')
def manga_scraper_app():
    return 'Hello, World!'