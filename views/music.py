from flask import Blueprint, render_template

import os
from plexapi.myplex import MyPlexAccount

music = Blueprint('music', __name__)

PREV_USERNAME = None
PREV_PASSWORD = None
PREV_SERVER_NAME = None
SERVER = None
ALBUM_CACHE = {}

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

def get_track_year(track):
    global ALBUM_CACHE

    album_identifier = (track.parentTitle, track.grandparentTitle)
    if not album_identifier in ALBUM_CACHE.keys():
        ALBUM_CACHE[album_identifier] = track.album()

    return ALBUM_CACHE[album_identifier]

def combine_indices(disk_number, track_number):
    left = str(disk_number) + '-'
    right = str(track_number)

    if str(disk_number) in ['1', None]:
        left = ''
    else:
        right = right.rjust(2, '0')

    return left + right

def track_to_dict(track):
    return {
        '_disk_number': track.parentIndex,
        '_index': track.index,
        'index': combine_indices(track.parentIndex, track.index),
        'title': track.title,
        'album': track.parentTitle,
        'artist': track.originalTitle,
        'album_artist': track.grandparentTitle,
        'year': get_track_year(track).year,
    }

def retrieve_tracks(music_library, rating):
    tracks = music_library.search(libtype='track', **{'track.userRating': rating})
    tracks = map(track_to_dict, tracks)
    tracks = sorted(tracks, key=lambda track: (track['album_artist'], track['year'], track['_disk_number'], track['_index']))
    return list(tracks)

@music.route('/music/')
def index():
    username = os.environ.get('CFG_PLEX_USERNAME')
    password = os.environ.get('CFG_PLEX_PASSWORD')
    server_name = os.environ.get('CFG_PLEX_SERVER_NAME')

    server = get_server(username, password, server_name)
    music = server.library.section('Music')

    five_star_tracks = retrieve_tracks(music, rating=10)
    four_star_tracks = retrieve_tracks(music, rating=8)
    # three_star_tracks = retrieve_tracks(music, rating=6)

    return render_template('music/index.html', **{
        'five_star_tracks': five_star_tracks,
        'four_star_tracks': four_star_tracks,
        # 'three_star_tracks': three_star_tracks
    })
