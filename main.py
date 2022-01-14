from src.cli import *
from src.repositories import Cities, Streets
from sys import argv
from collections import Counter

mapbox = get_mapbox(argv)

cities = Cities("data/SIMC_Urzedowy_2021-10-09.csv")
streets = Streets("data/ULIC_Adresowy_2021-10-09.csv", cities)
menu()
option = int(input("Enter your option: "))
if option == 1:
    searched_street = input("Give street name to seek: \n")
    counter = 0
    found_streets = streets.find_by_street_name(searched_street)

    for street in found_streets:
        phrase = str(street.city) + ": " + street.get_full_name()
        print(phrase)
        counter = counter + 1

        if mapbox:
            coordinate = mapbox.add_coordinates_for_phrase(phrase)

    print(str(counter) + " streets were found.")

if option == 2:
    streets.compare_two_streets_popularity(streets)
if option == 3:
    streets.find_most_popular_streets_100()
if option == 4:
        cities.find_most_popular_city_names_20()
if option == 5:
    streets.find_most_popular_street_in_voivodeship()
if option == 6:
    streets.count_street_type_in_country()
if option == 7:
    streets.count_street_type_in_city()
if option == 8:
    streets.find_same_streets_in_city()



if mapbox:
    mapbox.prepare_map(searched_street)


