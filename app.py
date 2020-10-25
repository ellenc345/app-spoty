from flask import Flask, render_template
import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

image_placeholder = '/statis/images/dog.png'
my_user_id = '213etedkqiwnnpl3qzb3qvwgq'


def make_header(token):
    bearer_token = f'{token.get("token_type")} {token.get("access_token")}'
    return {'Authorization': bearer_token}

def authenticato_spoty():
    SPOTIFY_SECRET_KEY = os.environ.get("SPOTIFY_SECRET_KEY")
    SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")

    res = requests.post(url="https://accounts.spotify.com/api/token",
                          auth=(SPOTIFY_CLIENT_ID, SPOTIFY_SECRET_KEY),
                          data={"grant_type": "client_credentials"})

    return make_header(json.loads(res.content))

def get_image_url(playlist):
    images = playlist.get('images')
    if images and len(images):
        return images[0].get('url')
    else:
        return image_placeholder

def playlists_covers(header):
    url = f"https://api.spotify.com/v1/users/{my_user_id}/playlists?limit=4&offset=0"
    res = requests.get(url, headers=header)
    playlists = json.loads(res.content)
    covers = []
    for playlist in playlists.get("items"):
        covers.append(get_image_url(playlist))
    print(len(covers))
    return covers

def load_data():
    header = authenticato_spoty()
    covers = playlists_covers(header)
    return covers

@app.route('/')
def hello_world():
    covers = load_data()
    return render_template('index.html', covers=covers, my_user_id=my_user_id)


if __name__ == '__main__':
    os.environ['PYTHONPATH'] = os.getcwd()
    app.run(threaded=True)
