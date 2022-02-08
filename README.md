# 01_Lab_Spring_2022
This is the project that works with dataset of films and their shooting locations.
Technologies used: 
*Nominatim for geocoding
*Folium module for making web maps
*Argparse for command line interface

## Usage
Module is called from the command line
```bash
python3 main.py 2004 49.83826 24.02324 1000_locations.list
```

User specifies the year, his/her location and the path to the dataset.
In order to parse whole dataset, user have to set the year to **-1**

Test datasets are included. One contains only films shot in Ukraine. The other contains 1000 random movies from all around the world

If many filmes were shoot on the same location, pictograms will form a spiral as shown on the screenshot:

![spiral](https://github.com/rwmutel/01_Lab_Spring_2022/blob/master/output%20examples/spiral.png)

## Summary
Module receives input from the user and creates **films.html** file with an interactive web map, containing all the movies shot in the specific time (blue layer).
Purple layer shows movies shot on the 10 closest locations to user coordinates. **Note** that there may be more than 10 films if some of them were shot on the same location.

Here is an example of the all films, shot in Ukraine. User location is set to Lviv.

![](https://github.com/rwmutel/01_Lab_Spring_2022/blob/master/output%20examples/ukrainian_locations_all_Lviv.png)

Another example of films shot in 2004 all around the world. User location is set to Lviv.

![](https://github.com/rwmutel/01_Lab_Spring_2022/blob/master/output%20examples/1000_locations_2004_Lviv.png)
