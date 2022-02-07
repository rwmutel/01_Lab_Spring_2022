import argparse
import folium
from geopy.geocoders import Nominatim

'''
A module for creating a map showing 10 closest
filming locations.
User specifies the year of films and the coordinates.
'''

def read_arguments():
    '''
    A function to read arguments using argparse module and return them as a tuple
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=int, help='Year of the films')
    parser.add_argument('lattitude', type=float, help='Your lattitude')
    parser.add_argument('longtitude', type=float, help='Your longtitude')
    parser.add_argument('path', help='Path to film dataset')
    args = parser.parse_args()
    return args.year, args.lattitude, args.longtitude, args.path


def make_map():
    gl = Nominatim(user_agent="mutel's 01_lab project")
    film_map = folium.Map(location=[49.8327787, 23.9421956])
    ukr = folium.FeatureGroup(name='Films shoot in Ukraine')

    with open('ukraine_locations.list') as src:
        data = src.readlines()
        known_locations = dict()
        for film in data:
            film = film.strip().split('\t')
            coordinates = ''
            location = film[-1]

            if film[-1].startswith('('):
                location = film[-2]

            if location in known_locations:
                coordinates = known_locations[location]
            else:
                coordinates = gl.geocode(location)
                i = 1
                while coordinates is None:
                    coordinates = gl.geocode(','.join(location.split(', ')[i:]))
                    i += 1
                known_locations[location] = coordinates

            print(location, film[0])
            ukr.add_child(folium.Marker(name=film[0], 
                location=(coordinates.latitude, coordinates.longitude), 
                popup=folium.Popup()))

    film_map.add_child(ukr)
    film_map.add_child(folium.LayerControl())
    film_map.save('nearby_films.html')

if __name__ == '__main__':
    make_map()
    args = read_arguments()
    print(args)