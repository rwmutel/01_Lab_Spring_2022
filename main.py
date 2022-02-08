import argparse
from math import cos, pi, sin
import folium
from geopy.geocoders import Nominatim
from geopy.distance import great_circle

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


def make_map(user_map: folium.Map, dataset: str = 'ukraine_locations.list') -> folium.Map:
    """
    Parces data from the dataset
    Adds a layer with those films to the user_map
    Saves modified map as 'all_films.html'
    Returns modified user_map

    Args:
        user_map (folium.Map): map object to be modified
        dataset (str): path to the dataset ('ukraine_locations.list' by default)

    Returns:
        folium.Map: user_map with a layer containing all the film shooting locations
    """

    gl = Nominatim(user_agent="mutel's 01_lab project")
    film_map = user_map
    locs = folium.FeatureGroup(name='All Shooting Locations')

    with open(dataset) as src:
        data = src.readlines()
        known_locations = dict()
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

                radius = appearance * ONE_KM / 20
                degree = appearance * pi / 12
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

            locs.add_child(folium.Marker(name=film[0], 
                location=(display_lat, display_lon), 
                popup=film[0]))

    film_map.add_child(locs)
    film_map.save('all_films.html')

    with open('cached_locations.csv', mode='w') as cached:
        for key in known_locations:
            cached.write(','.join([key.replace(',', '.'),
                str(known_locations[key][0].latitude),
                str(known_locations[key][0].longitude)]) + '\n')

    return film_map


def make_closest_map(user_map: folium.Map, lat: float, lon: float, year: int = -1,\
    dataset: str = 'ukraine_locations.list', cached: str='cached_locations.csv')-> folium.Map:
    """
    Adds a layer to a .html map of the ten closest film locations
    User passes the location and the year of films to be mapped
    Saves final result as 'closest_films.html'
    Returns the resulting map for further usage

    Args:
        user_map (folium.Map): map, on which the locations will be added
        lat (float): user latitude
        lon (float): user longitude
        year (int): year of the films
        cached (str): path to a .csv file (cached_locations.csv).
            This file is created after make_map() function call.

    Returns:
        folium.Map: resulting map
    """

    film_map = user_map
    closest = folium.FeatureGroup(name='10 closest UA film locations')
    closest_locations = [('', -1)] * 10
    cached_locations = dict()

    with open(cached, mode='r') as cache:
        entry = cache.readline()
        while entry != '':
            location, l_lat, l_lon = entry.split(',')
            cached_locations[location] = (float(l_lat), float(l_lon))
            l_distance = great_circle((lat, lon), (float(l_lat), float(l_lon[:-2])))
            for _, closest_location in enumerate(closest_locations):
                if l_distance < closest_location[1] or closest_location[1] == -1:
                    closest_locations.insert(_, (location, l_distance))
                    closest_locations.pop()
                    break
            entry = cache.readline()

    with open(dataset, mode='r') as src:
        mapped_locations = dict()
        entry = src.readline()
        ONE_KM = 0.009

        while entry != '':
            entry = entry.split('\t')
            film = entry[0]
            film_year = film[film.find('(')+1:film.find('(')+5]

            location = entry[-1].replace(',', '.').strip()
            if location.startswith('('):
                location = entry[-2].replace(',','.').strip()

            entry = src.readline()

            if location not in list(map(lambda x:x[0], closest_locations)):
                continue

            if year != -1 and (film_year == '????' or film_year != str(year)):
                continue

            if location in mapped_locations:
                appearance = mapped_locations[location]
                mapped_locations[location] += 1
                radius = appearance * ONE_KM / 20
                degree = appearance * pi / 12
                display_lat = cached_locations[location][0] + radius * sin(degree)
                display_lon = cached_locations[location][1] + radius * cos(degree)
            else:
                mapped_locations[location] = 1
                display_lat = cached_locations[location][0]
                display_lon = cached_locations[location][1]

            closest.add_child(folium.Marker(name=film, 
                location=(display_lat, display_lon), 
                popup=film, icon=folium.Icon(color='purple')))

    film_map.add_child(closest)
    film_map.save('closest_films.html')
    return film_map


if __name__ == '__main__':
    year, lat, lon, path = read_arguments()
    main_map = folium.Map(location=(lat,lon))
    main_map = make_map(main_map, path)
    main_map = make_closest_map(main_map, lat, lon, dataset=path)
    main_map.add_child(folium.LayerControl())
    main_map.save('films.html')
    print('Done! Open films.html to see the result')
