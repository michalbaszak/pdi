from src.places import City, Street

from collections import Counter
import csv
class Cities(object):
    def __init__(self, file):
        self.file = file

    def find_by_id(self, city_id):
        with open(self.file, encoding="utf-8") as fp:
            lines = fp.readlines()
            city = self.__find_exact_city(lines, city_id)

            if not city:
                city = self.__find_fallback_city(lines, city_id)

            if city:
                return city

        return City("? (" + city_id + ")")

    def find_most_popular_city_names_20(self):
        score = []
        with open(self.file, encoding="utf-8") as file:
            data = list(csv.reader(file))
            for row in data[1:-1]:
                row = str(row).split(";")
                score.append(row[6])
            c = Counter(score)

            for city, count in c.most_common(20):
                print('%s: %d' % (city, count))

    @staticmethod
    def __find_exact_city(lines, city_id):
        for line in lines:
            if city_id + ";" + city_id in line:
                return City(line.split(";")[6])

    @staticmethod
    def __find_fallback_city(lines, city_id):
        for line in lines:
            if city_id in line:
                return City(line.split(";")[6])

    def find_by_name(self, city_name):
        with open(self.file, encoding="utf-8") as file:
            city_id = []
            csv_reader = csv.reader(file)
            data = list(csv_reader)
            for row in data[1:-1]:
                row = str(row).split(";")
                line = row[6].split('-', 1)
                if line[0] == city_name:
                    city_id.append(row[7])
            return city_id
            # elif city_name == row[6]:
            #     city_id.append(row[7])
            # city_id = []
            # lines = file.readlines()
            # for line in lines:
            #     if city_name in line:
            #         city_id.append(line.split(";")[7])
            #         # return City(line.split(";")[7])
            # return city_id
class Streets(object):
    def __init__(self, file, cities):
        self.file = file
        self.cities = cities

    def find_by_street_name(self, street_name):
        with open(self.file, encoding="utf-8") as fp:
            lines = fp.readlines()
            for line in lines:
                if street_name.lower() in line.lower():
                    street = Street(line)
                    street.set_city(self.cities.find_by_id(street.city_id))
                    yield street

    def compare_two_streets_popularity(self, streets):

        first_street = input("Give first street name to compare: ")
        second_street = input("Give second street name to compare: ")
        counter_1 = 0
        first_streets_found = streets.find_by_street_name(first_street)
        for street in first_streets_found:
            counter_1 = counter_1 + 1

        counter_2 = 0
        second_streets_found = streets.find_by_street_name(second_street)
        for street in second_streets_found:
            counter_2 = counter_2 + 1

        print(str(counter_1) + " streets found with phrase " + str(first_street) + ".")
        print(str(counter_2) + " streets found with phrase " + str(second_street) + ".")

    def find_most_popular_streets_100(self):
        score = []
        with open(self.file, encoding="utf-8") as file:
            data = list(csv.reader(file))
            for row in data[1:-1]:
                row = str(row).split(";")
                score.append(row[8] + " " + row[7])
            c = Counter(score)

            for street, count in c.most_common(100):
                print('%s: %d' % (street, count))

    def find_most_popular_street_in_voivodeship(self):
        voivodeships_names = ("Dolnośląskie", "Kujawsko-Pomorskie", "Lubelskie", "Lubuskie", "Łódzkie",
                             "Małopolskie", "Mazowieckie", "Opolskie", "Podkarpackie", "Podlaskie",
                             "Pomorskie", "Śląskie", "Świętokrzyskie", "Warmińsko-Mazurskie", "Wielkopolskie",
                             "Zachodniopomorskie")

        with open(self.file, encoding="utf-8") as file:
            data = list(csv.reader(file))
            for n in voivodeships_names:
                voivodeship_id = 2 + (voivodeships_names.index(n) * 2)
                score = []
                for row in data[1:-1]:
                    row = str(row).split(";")
                    if int(row[0][-2:]) == voivodeship_id:
                        score.append(row[8] + " " + row[7])
                c = Counter(score)

                for street, count in c.most_common(1):
                    print('%s: %s %d' % (n, street, count))

    def count_street_type_in_country(self):
        score = []
        with open(self.file, encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            data = list(csv_reader)
            for row in data[1:-1]:
                row = str(row).split(";")
                score.append(row[6])
            c = Counter(score)

            for type_street, count in c.most_common():
                if type_street:
                    print('%s- %d' % (type_street, count))
                else:
                    print('%s- %d' % ("undefined", count))

    def count_street_type_in_city(self):
        city_name = input("Give city name: ")
        city_id = self.cities.find_by_name(city_name)
        score = []
        with open(self.file, encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            data = list(csv_reader)
            for row in data[1:-1]:
                row = str(row).split(";")
                for id in city_id:
                    if str(id) == row[4]:
                        score.append(row[6])
            c = Counter(score)
            print('%s:' % (city_name))
            for type_street, count in c.most_common(10):
                if type_street:
                    print('%s- %d' % (type_street, count))
                else:
                    print('%s- %d' % ("undefined", count))

    def find_same_streets_in_city(self):
        city_name = input("Give city name: ")
        score = []
        with open(self.file, encoding="utf-8") as file:
            city_id = self.cities.find_by_name(city_name)
            csv_reader = csv.reader(file)
            data = list(csv_reader)
            for row in data[1:-1]:
                row = str(row).split(";")
                for id in city_id:
                    if str(id) == row[4]:
                        score.append(row[7])
            c = Counter(score)
            print('%s:' % (city_name))
            for street, count in c.most_common(100):
                if count > 1:
                    print('%s- %d' % (street, count))



