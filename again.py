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




def citiesserved(cityList, distanceList, name, r): #this function should find the number of unserved
    served = [False] * len(cityList)                         #cities within distance r of the city
    a = nearbyCities(cityList,distanceList, name, r)
    city_index = cityList.index(name)
    served[city_index] = True
    for name in a:
        city_index = cityList.index(name)
        served[city_index] = True
    return served

def find_best_city_to_start(cityList,distanceList, r):
    best_amount_of_served = 0
    best_city = ""
    for name in cityList:
        bool_list = citiesserved(cityList,distanceList,name, r)
        temp_count = bool_list.count(True)
        if temp_count > best_amount_of_served:
            best_amount_of_served = temp_count
            best_city = name
    return best_city

def removeserved(served, cityList):
    for i in range(len(served)):
        if served[i] ==True:
            cityList.remove(cityList[i])
    for value in served:
        if value == True:
            served.remove(value)
    return served

def locatefacilities(cityList,distanceList,r):
    name = find_best_city_to_start(cityList, distanceList, r)
    served = citiesserved(cityList, distanceList, name, r)
    facilities = [name]
    unserved = removeserved(served,cityList)
    # REMOVE THE BEST CITY AND ITS SERVED FROM THE LIST SO ONLY FALSE VALUES EXIST
    while False in unserved:
        best_count = 0
        best_city = ""
        for name in cityList:
            temp_served = citiesserved(cityList, distanceList, name, r)
            count = 0
            for value in temp_served:
                if value == True:
                    count +=1
            if count > best_count:
                best_count = count
                best_city = name
        facilities.append(best_city)
        name = best_city
        unserved = citiesserved(cityList, distanceList, name, r)
    return facilities










# main program
cityList = []
coordList = []
popList = []
distanceList = []

loadData(cityList, coordList, popList, distanceList)






# Fix coordinates empty list issue
# is long or lat first in coord list and
# does every longitude value need to be negative?
# which needs to be first in kml format
# for the line, how are the coordinates formatting in kml
# how to save the kml files I have made ?

#create other pretty things like circle of influence
# If you wish, you could have push pins of one color at facilities and push pins of a different color at cities that don't have facilities.

#What does this MEAN?
    # You could call locateFacilities once with r = 300, and get a list of facilites, say fac300.
    #Call locateFacilities a second time with r = 800, and get a list of facilites, say fac800.
    # Then call display twice, once with fac300 and once with fac800.
    # You might also want to send in the two filenames as arguments to display.


