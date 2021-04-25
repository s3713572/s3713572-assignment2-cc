from music import app
from music.seeds import create_10_logins, create_music_table, load_json_data
import json
from decimal import Decimal




if __name__ == '__main__':
    create_music_table()
    create_10_logins()
    with open("a2.json") as json_file:
        movie_list = json.load(json_file, parse_float=Decimal)
    load_json_data(movie_list)
    app.run(debug=True,host='0.0.0.0',threaded=True)