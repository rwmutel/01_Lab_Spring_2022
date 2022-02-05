import argparse
import folium

'''
A module for creating a map showing 10 closest
filming locations.
User specifies the year of films and the coordinates.
'''

def read_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=int, help='Year of the films')
    parser.add_argument('lattitude', type=float, help='Your lattitude')
    parser.add_argument('longtitude', type=float, help='Your longtitude')
    parser.add_argument('path', help='Path to film dataset')
    args = parser.parse_args()
    return args.year, args.lattitude, args.longtitude, args.path

if __name__ == '__main__':
    args = read_arguments()
    print(args)