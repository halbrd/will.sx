from flask import Blueprint, render_template

import os
from plexapi.myplex import MyPlexAccount

music = Blueprint('music', __name__)

PREV_USERNAME = None
PREV_PASSWORD = None
PREV_SERVER_NAME = None
SERVER = None

def creds_are_same(username, password, server_name):
    global PREV_USERNAME, PREV_PASSWORD, PREV_SERVER_NAME
    return (username, password, server_name) == (PREV_USERNAME, PREV_PASSWORD, PREV_SERVER_NAME)

def get_server(username, password, server_name):
    global SERVER, PREV_USERNAME, PREV_PASSWORD, PREV_SERVER_NAME

    if SERVER is None or not creds_are_same(username, password, server_name):
        account = MyPlexAccount(username, password)
        SERVER = account.resource(server_name).connect()

    PREV_USERNAME, PREV_PASSWORD, PREV_SERVER_NAME = username, password, server_name

    return SERVER

@music.route('/music/')
def index():
    username = os.environ.get('CFG_PLEX_USERNAME')
    password = os.environ.get('CFG_PLEX_PASSWORD')
    server_name = os.environ.get('CFG_PLEX_SERVER_NAME')

    server = get_server(username, password, server_name)
    music = server.library.section('Music')

    five_star_tracks = music.search(libtype='track', **{'track.userRating': 10})
    four_star_tracks = music.search(libtype='track', **{'track.userRating': 8})
    three_star_tracks = music.search(libtype='track', **{'track.userRating': 6})

    return render_template('music/index.html', **{
        'five_star_tracks': five_star_tracks,
        'four_star_tracks': four_star_tracks,
        'three_star_tracks': three_star_tracks
    })
