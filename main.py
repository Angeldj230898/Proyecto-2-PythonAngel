from flask import Flask, jsonify, request
from flask_cors import CORS
from uuid import uuid1 # generador de id's

# datos
from songs import songs as songs_list
from users import users as users_list
from comments import comments as comments_list
from playlists import playlists


app = Flask(__name__)
CORS(app)

# ================================================================================

# obtener canciones
@app.route('/songs')
def get_songs():
  response = []

  for song in songs_list:
    if song['state'] == 1:
      response.append(song)

  return jsonify({'songs':response})


# obtener canciones por nombre
@app.route('/songs/<string:name>/name')
def get_songs_by_name(name):
  response = []

  for song in songs_list:
    if song['state'] == 1:
      if name in song['name']:
        response.append(song)

  return jsonify({'songs':response})


# obtener canciones en solicitud
@app.route('/songs/requested')
def get_sogs_requested():
  response = []

  for song in songs_list:
    if song['state'] == 0:
      response.append(song)

  return jsonify({'songs':response})


# obtener una cancion por su id
@app.route('/songs/<string:id>')
def get_song(id):
  response = []

  for song in songs_list:
    if song['id'] == id:
      response.append(song)
      break

  return jsonify({'song':response})


# crear una cancion
@app.route('/songs', methods=['POST'])
def add_song():
  song = {
      "album": request.json['album'],
      "author": request.json['author'],
      "date": request.json['date'],
      "id": str(uuid1()),
      "name": request.json['name'],
      "spotify": request.json['spotify'],
      "state": 1,
      "youtube": request.json['youtube']
    }
  songs_list.append(song)

  songs = []

  for song in songs_list:
    if song['state'] == 1:
      songs.append(song)

  return jsonify({'message': 'okay', 'songs': songs})


# pedir una cancion
@app.route('/song/request', methods=['POST'])
def request_song():
  song = {
      "album": request.json['album'],
      "author": request.json['author'],
      "date": request.json['date'],
      "id": str(uuid1()),
      "name": request.json['name'],
      "spotify": request.json['spotify'],
      "state": 0,
      "youtube": request.json['youtube']
    }
  songs_list.append(song)

  songs = []

  for song in songs_list:
    if song['state'] == 0:
      songs.append(song)

  return jsonify({'code': 200, 'songs': songs})


# editar datos de una cancion
@app.route('/songs/<string:id>/edit', methods=['PUT'])
def update_song(id):
  i = 0
  for song in songs_list:
    if song['id'] == id:
      songs_list[i] = {
        "album": request.json['album'],
        "author": request.json['author'],
        "date": request.json['date'],
        "id": song['id'], # esta no es actualiza
        "name": request.json['name'],
        "spotify": request.json['spotify'],
        "state": song['state'], # esta no es actualiza
        "youtube": request.json['youtube']
      }

      return jsonify({'message': 'okay', 'song': songs_list[i]})

    i += 1

  return jsonify({'message': 'not found'})


# eliminar una cancion por su id
@app.route('/songs/<string:id>/delete', methods=['DELETE'])
def delete_song(id):
  for song in songs_list:
    if song['id'] == id:
      songs_list.remove(song) # esto elimina la cancion

      return jsonify({'message': 'okay'})

  return jsonify({'message': 'not found'})


# aceptar una cancion
@app.route('/songs/<string:id>/accept', methods=['PUT'])
def accept_song(id):
  i = 0
  for song in songs_list:
    if song['id'] == id:
      song_data = song
      songs_list.remove(song)
      
      song_data['state'] = 1
      songs_list.append(song_data)

      print(songs_list)

      return jsonify({'message': 'okay'})
  i += 1

  return jsonify({'message': 'not found'})


# comentarios
@app.route('/songs/<string:id>/comments')
def get_comments(id):
  comments = []

  for comment in comments_list:
    if comment['song'] == id:
      comments.append(comment)

  return jsonify({'comments': comments})


# nuevo comentario
@app.route('/songs/comments/new', methods=['POST'])
def create_comment():
  new_comment = {
    'user': request.json['user'],
    'text': request.json['text'],
    'song': request.json['song']
  }

  comments_list.append(new_comment)

  return jsonify({'code': 200, 'message': 'okay'})

# ================================================================================

# obtener usuaros
@app.route('/users')
def get_users():
  return jsonify({'users':users_list})


# inicio de sesion
@app.route('/auth/signin', methods=['POST'])
def signin():
  username = request.json['username']
  password = request.json['password']

  for user in users_list:
    if user['username'] == username:
      if user['password'] == password:
        the_user = user.copy()
        del the_user['password']
        return jsonify({'isloggedIn': True, 'user': the_user})

  return jsonify({'isloggedIn': False })


# registro de usuarios
@app.route('/auth/signup', methods=['POST'])
def signup():
  new_user = {
    'name': request.json['name'],
    'lastname': request.json['lastname'],
    'password': request.json['password'],
    'username': request.json['username'],
    'auth': 0,
  }

  for user in users_list:
    if user['username'] == new_user['username']:
      return jsonify({'isRegister': False, 'code':'REPEATED_NAME'})

  users_list.append(new_user)
  return jsonify({'isRegister': True})


# recuperar contrase;a
@app.route('/auth/password', methods=['POST'])
def get_password():
  username = request.json['username']

  for user in users_list:
    if user['username'] == username:
      return jsonify({'password': user['password']})

  return jsonify({'password': None, 'code':'USER_NOT_FOUND'})


@app.route('/users/<string:id>/update', methods=['PUT'])
def edit_user(id):
  i = 0
  for user in users_list:
    if user['id'] == id:
      users_list[i] = {
        'id': user['id'],
        'name': request.json['name'],
        'lastname': request.json['lastname'],
        'password': request.json['password'],
        'username': request.json['username'],
        'auth': user['auth']
      }

      return jsonify({'message': 'okay', 'code': 200})

    i += 1

  return jsonify({'message': 'not found', 'code': 404})


@app.route('/users/<string:id>/data')
def datos_usuario(id):

  for user in users_list:
    if user['id'] == id:
        return jsonify({'user': user})


# ================================================================================

# obtener canciones de mi playlist
@app.route('/playlist/<string:id>/user')
def get_playlist(id):
  songs = []

  for record in playlists:
    user = record['user']

    if user == id:
      songs.append(record['song'])

  return jsonify({'code': 200, 'songs': songs})


# agregar cancion a playlist
@app.route('/playlist/add', methods=['POST'])
def add_to_playlist():
  playlists.append({
    'user': request.json['user']['id'],
    'song': request.json['song']
  })

  return jsonify({'code': 200})


if __name__ == '__main__':
  app.run(debug=True, port=4000) # iniciar API
