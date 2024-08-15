import simplekml
import subprocess
import pandas as pd

def extractCityStateNames(line):
    pieces = line.split(",")
    return pieces[0] + pieces[1][:3]


def extractCoordinates(line):
    pieces = line.split(",")
    return [int(pieces[1].split("[")[1]), int(pieces[2].split("]")[0])]


def extractPopulation(line):
    pieces = line.split(",")
    return int(pieces[2].split("]")[1])


def loadData(cityList, coordList, popList, distanceList):
    f = open("miles.dat")

    # Tracks which city we are currently processing
    cityIndex = 0

    # Keeps track of distances from current city to previous cities
    distances = []
    distanceList.append([])

    # Reads from the file, one line at a time
    for line in f:

        # Checks if the line is a "city line", i.e., contains information about
        # the city
        if line[0].isalpha():

            # Distances from the previous city need to be loaded into distanceList
            if distances != []:
                distanceList.append(distances[::-1])
                distances = []

            cityList.append(extractCityStateNames(line))
            coordList.append(extractCoordinates(line))
            popList.append(extractPopulation(line))
            cityIndex = cityIndex + 1

        # Checks if the line is a "distance line", i.e., contains information
        # distances from this city to previous cities
        elif line[0].isdigit():
            distances.extend([int(x) for x in line.split()])

    # Distances from the previous city need to be loaded into distanceList
    if distances != []:
        distanceList.append(distances[::-1])


def getCoordinates(cityList, coordList, name):
    return coordList[cityList.index(name)]


def getPopulation(cityList, popList, name):
    return popList[cityList.index(name)]


def getDistance(cityList, distanceList, name1, name2):
    index1 = cityList.index(name1)
    index2 = cityList.index(name2)

    if index1 == index2:
        return 0
    elif index1 < index2:
        return distanceList[index2][index1]
    else:
        return distanceList[index1][index2]


def nearbyCities(cityList, distanceList, name, r):
    # The list result will eventually contain the names of cities
    # at distance <= r from name
    result = []

    # Get the index of the named city in cityList
    i = cityList.index(name)

    # Walk down the distances between the named city and previous cities
    j = 0
    for d in distanceList[i]:  # For every other previous city
        if d <= r:  # If within r of named city
            result = result + [cityList[j]]  # Add to result
        j = j + 1

    # Walk down the distances between the named city and later cities
    j = i + 1
    while (j < len(distanceList)):  # For every other previous city
        if distanceList[j][i] <= r:  # If within r of named city
            result = result + [cityList[j]]  # Add to result

        j = j + 1

    return result


def bool_list(cityList, distanceList, name, r):
    first_bool = [False] * len(cityList)
    L = nearbyCities(cityList, distanceList, name, r)
    city_index = cityList.index(name)
    first_bool[city_index] = True
    for name in L:
        ind = cityList.index(name)
        first_bool[ind] = True
    return first_bool


def find_best_city(served, facilities, cityList, distanceList, r):
    best_served = 0
    best_city = ""
    for name in cityList:
        count = 0
        if name not in facilities:
            temp_served = bool_list(cityList, distanceList, name, r)
            for i in range(len(temp_served)):
                if temp_served[i] == True and served[i] == False:
                    count += 1
            if count > best_served:
                best_served = count
                best_city = (name)
    return best_city


def updateList(served, cityList, distanceList, name, r):
    temp_bool = bool_list(cityList, distanceList, name, r)
    updated_served = []
    for i in range(len(temp_bool)):
        if temp_bool[i] == True and served[i] == True:
            updated_served.append(True)
        elif temp_bool[i] == False and served[i]== True:
            updated_served.append(True)
        elif temp_bool[i] == True and served[i] == False:
            updated_served.append(True)  # had this as false
        elif temp_bool[i] == False and served[i] == False:
            updated_served.append(False)

    return updated_served


def locateFacilities(cityList, distanceList, r):
    served = [False] * len(cityList)
    facilities = []
    # for value in served:
    #     if value == True:
    #         continue
    #     else:
    while False in served:
            name = find_best_city(served, facilities, cityList, distanceList, r)
            facilities.append(name)
            served = updateList(served, cityList, distanceList, name, r)
    return facilities



def display(facilities, cityList, distanceList, coordList):
    coordList = [[float(x/100) for x in sublist]for sublist in coordList]
    if facilities == locateFacilities(cityList, distanceList, 800):                                                                #call display 800
        facilities = locateFacilities(cityList, distanceList, 800)
        display800(facilities, cityList, distanceList, coordList)
        # need to get all nearby cities for each facility. draw a line from city to the nearby city.
    else:                                                               #call display 300
        facilities = locateFacilities(cityList, distanceList, 300)
        display300(facilities, cityList, distanceList, coordList)



def display800(facilities, cityList, distanceList, coordList):
    with open('visualization800.kml', 'w') as f:
        # boilerplate for initializing a kml file
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write('<Document>\n\n')

        f.write('<Style id="pin">\n')
        f.write(' <BalloonStyle>\n')
        f.write('   <color>ff0000ff</color>\n')
        f.write('   <text> <![CDATA[<b>Test Text</b>]]></text>\n')
        f.write(' </BalloonStyle>\n')
        f.write('</Style>\n\n')

        f.write('<Style id = "yellowLine">\n')
        f.write(' <linestyle>\n')
        f.write('   <color>7f00ffff</color>\n')
        f.write('   <width>10</width>\n')
        f.write(' </linestyle>\n')
        f.write('</Style>\n\n')

        for name in facilities:
            ind = cityList.index(name)
            # creating a 'style' for our placemark              #DOES THIS NEED TO COME FIRST????
            # actually dropping the pin, using python f-str
            f.write('<Placemark>\n')
            f.write(f' <name>{name}</name>\n')
            f.write(' <styleUrl>#pin</styleUrl>\n')
            f.write(' <Point>\n')
            f.write(f'  <coordinates>-{(coordList[ind][1])},{(coordList[ind][0])},0 </coordinates>\n')     #PROBLEM AREA
            f.write(' </Point>\n')
            f.write('</Placemark>\n\n')
            for name1 in cityList:
                if name1 not in facilities:
                    closfac = findFacility(facilities, cityList, name1)
                    fac = cityList.index(closfac)
                    c = cityList.index(name1)
                    long = coordList[fac][1]
                    lat = coordList[fac][0]
                    f.write('<Placemark>\n')
                    f.write(f' <name>{closfac} to {name1}</name>\n')
                    f.write(' <styleUrl>#yellowLine</styleUrl>\n')
                    f.write(' <LineString>\n')
                    f.write(f'  <coordinates>-{long},{lat},0 -{coordList[c][1]},{(coordList[c][0])},0</coordinates>\n')
                    f.write(' </LineString>\n')
                    f.write('</Placemark>\n\n')
        f.write('</Document>\n')
        f.write('</kml>')
        f.close()


def display300(facilities, cityList, distanceList, coordList):
    with open('visualization300.kml', 'w') as f:
        # boilerplate for initializing a kml file
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write('<Document>\n\n')

        f.write('<Style id="pin">\n')
        f.write(' <BalloonStyle>\n')
        f.write('   <color>ff0000ff</color>\n')
        f.write('   <text> <![CDATA[<b>Test Text</b>]]></text>\n')
        f.write(' </BalloonStyle>\n')
        f.write('</Style>\n\n')

        f.write('<Style id="yellowLine">\n')
        f.write(' <linestyle>\n')
        f.write('   <color>7f00ffff</color>\n')
        f.write('   <width>10</width>\n')
        f.write(' </linestyle>\n')
        f.write('</Style>\n\n')

        for name in facilities:
            ind = cityList.index(name)
            # creating a 'style' for our placemark
            # actually dropping the pin, using python f-string
            f.write('<Placemark>\n')
            f.write(f' <name>{name}</name>\n')
            f.write(' <styleUrl>#pin</styleUrl>\n')
            f.write(' <Point>\n')
            f.write(f'  <coordinates>-{coordList[ind][1]},{coordList[ind][0]},0</coordinates>\n')
            f.write(' </Point>\n')
            f.write('</Placemark>\n\n')
        for name1 in cityList:
            if name1 not in facilities:
                closfac = findFacility(facilities,cityList,name1)
                fac = cityList.index(closfac)
                c = cityList.index(name1)
                long = coordList[fac][1]
                lat = coordList[fac][0]
                f.write('<Placemark>\n')
                f.write(f' <name>{closfac} to {name1}</name>\n')
                f.write(' <styleUrl>#yellowLine</styleUrl>\n')
                f.write(' <LineString>\n')
                f.write(f'  <coordinates>-{long},{lat},0 -{coordList[c][1]},{(coordList[c][0])},0</coordinates>\n')
                f.write(' </LineString>\n')
                f.write('</Placemark>\n\n')
        f.write('</Document>\n')
        f.write('</kml>\n')
        f.close()


cityList = []
coordList = []
popList = []
distanceList = []


loadData(cityList, coordList, popList, distanceList)

def findFacility(facilities, cityList, name1):
    closest_distance = 1000
    closest_facility = ""
    for name2 in facilities:
        distance = getDistance(cityList, distanceList, name1, name2)
        if distance < closest_distance:
            closest_distance = distance
            closest_facility = name2
    return closest_facility



facilities = locateFacilities(cityList, distanceList, 800)
display(facilities, cityList, distanceList, coordList)
facilities = locateFacilities(cityList, distanceList, 300)
display(facilities, cityList, distanceList, coordList)





# iterate over each city in cityList. You can use for city in cityList, but it will require indexing the cityList for the city name when you grab your coordinates. Alternatively, you could use for i in range(len(cityList))
# for each city, now iterate over every city in your output from locateFacilities (this should be a list of the cities where facilities were placed)
# from here, you can use getDistance to calculate the distance from the current city to each city in the list of facilities.
# store the city name of the facility with the shortest distance to the city from cityList
# use the indexes of the city name and the facility city name in cityList to determine what index of coordinates you need to grab for each.
# input the data collected into f.write calls for your line template


# I would do a for loop and walk down the cities to place a line. You could make a helper function that makes a list of
# all the cities connected to each facility and use this to determine the line's end points. Just a warning,
# nearbyCities will connect some cities to more than one facility. Make sure you only make a line to the closest
# facility. You can use the coordinate formatting from the first part of the sample code