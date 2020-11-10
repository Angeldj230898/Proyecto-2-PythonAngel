from uuid import uuid1 # generador de id's

songs = [
  {
    'id': str(uuid1()),
    'name': 'Hero Worship',
    'author': 'Michael Giacchino',
    'album': 'haha',
    'date': 'date1',
    'spotify': 'https://open.spotify.com/embed/track/3YapPdCk2YCKuxJWGUwCnF',
    'youtube': 'https://www.youtube.com/embed/slRDmpV6P8M',
    'state': 1 # aceptada
  },
  {
    'id': str(uuid1()),
    'name': 'Elastigirl is Back',
    'author': 'Michael Giacchino',
    'album': 'hehe',
    'date': 'date2',
    'spotify': 'https://open.spotify.com/embed/track/2mtPh005xkipPu8WtXCHRq',
    'youtube': 'https://www.youtube.com/embed/1f39F1eAqkk',
    'state': 0 # en solicitud
  }
]