import argparse
from math import cos, pi, sin
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


def make_ukr_map(user_map: folium.Map = folium.Map(location=[49.8327,23.9421]), year: int = 2017) \
    -> folium.Map:
    """
    Parces data from 'ukraine_locations.list'
    Adds a layer with films, shoot in Ukraine to the user_map
    Returns modified user_map

    Args:
        user_map (folium.Map): map object to be modified
        year (int): films of this year will be displayed

    Returns:
        folium.Map: user_map with a layer containing all the film shooting location in Ukraine
    """

    gl = Nominatim(user_agent="mutel's 01_lab project")
    film_map = user_map
    ukr = folium.FeatureGroup(name='All Films Shoot in Ukraine')

    with open('ukraine_locations.list') as src:
        data = src.readlines()
        known_locations = dict()
        radius = 0
        degree = 0
        ONE_KM = 0.009

        for film in data:
            film = film.strip().split('\t')
            coordinates = ''
            location = film[-1]

            if film[-1].startswith('('):
                location = film[-2]

            if location in known_locations:
                coordinates = known_locations[location][0]
                appearance = known_locations[location][1]
                known_locations[location][1] += 1

                radius = appearance * ONE_KM / 10
                degree = appearance * pi / 6
                display_lat = coordinates.latitude + radius * sin(degree)
                display_lon = coordinates.longitude + radius * cos(degree)
            else:
                coordinates = gl.geocode(location)
                i = 1
                while coordinates is None:
                    coordinates = gl.geocode(','.join(location.split(', ')[i:]))
                    i += 1
                display_lat = coordinates.latitude
                display_lon = coordinates.longitude
                known_locations[location] = [coordinates, 0]

            print(location, film[0])
            ukr.add_child(folium.Marker(name=film[0], 
                location=(display_lat, display_lon), 
                popup=film[0]))

    film_map.add_child(ukr)
    film_map.add_child(folium.LayerControl())
    film_map.save('films.html')

    with open('cached_ukr_locations.csv', mode='w') as cached:
        for key in known_locations:
            cached.write(','.join([key.replace(', ', '.'),
                str(known_locations[key][0].latitude),
                str(known_locations[key][0].longitude)]) + '\n')

    return film_map


if __name__ == '__main__':
    args = read_arguments()
    main_map = make_ukr_map()
    print(args)