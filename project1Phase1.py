def getCities(cityList):
    s = open("miles.dat", "r")
    character1 = "["
    character2 = ","
    i = 0
    for line in s:
        city = ""
        if line[0].isupper():
            indch = line.index(character1)
            city = line[:indch]
            indcom = city.index(character2)
            city = city[:indcom] + "" + city[indcom + 1:]
            cityList.append(city)
            i += 1





def gettingCoords(coordList):
    s = open("miles.dat", "r")
    char1 = "["
    char2 = "]"
    char3 = ","
    i = 0
    for line in s:
        coords = []
        if line[0].isupper():
            #locating latitude
            left_bound = line.index(char1)
            right_bound = line.rindex(char3)
            latitude = line[left_bound + 1: right_bound]
            coords.append(int(latitude))
            #locating longitude
            right_bound = line.index(char2)
            left_bound = line.rindex(char3)
            longitude = line[left_bound + 1: right_bound]
            coords.append(int(longitude))
            coordList.append(coords)
            i += 1



def gettingPops(popList):
    s = open("miles.dat")
    i = 0
    char = "]"
    for line in s:
        pop = ""
        if line[0].isupper():
            ind = line.index(char)
            digit = line[ind + 1:]
            pop += digit
            popList.append(int(pop))
            i+= 1



def gettingdistance(distanceList):
    distanceList.append([])
    i = 1
    j = 6
    char = [" "]
    with open("miles.dat", "r") as file:
        lines = file.readlines()[j:]
        distance = []
        for line in lines:
            currentdistance = ""
            if line[0].isdigit():
                for ch in line:
                    if ch.isdigit():
                        currentdistance += ch
                    elif ch == " ":
                        distance.append(int(currentdistance))
                        currentdistance = ""
                    else:
                        distance.append(int(currentdistance))
                        currentdistance = ""
            else:
                distanceList.append(distance)
                distance = []
                i += 1



def loadData(cityList, coordList, popList, distanceList):
    getCities(cityList)
    gettingCoords(coordList)
    gettingPops(popList)
    gettingdistance(distanceList)




def getCoordinates(cityList,coordList,name):
    if name in cityList:
        ind = cityList.index(name)
        return coordList[ind]
    else:
        return None


def getPopulation(cityList, popList, name):
    # this function returns the population of the city name.
    if name in cityList:
        ind = cityList.index(name)
        return popList[ind]
    else:
        return None

def getDistance(cityList, distanceList, name1, name2):
    # this function returns the distance between the two cities.
    ind1 = cityList.index(name1)
    ind2 = cityList.index(name2)
    if ind1 > ind2:
        ind1 = cityList.index(name2)
        ind2 = cityList.index(name1)
        distancelocation = int(ind2 - ind1)
        return distanceList[ind2][distancelocation - 1]
    if ind2 > ind1:
        distancelocation = int(ind2 - ind1)
        return distanceList[ind2][distancelocation -1]
    elif ind2 == ind1:
        return 0



def nearbyCities(cityList, distanceList, name, r):
        list_of_nearby_cities = []
        indcity = cityList.index(name)
        L = distanceList[indcity]
        L = L[::-1]
        for distance in L:
            if distance <= r:
                inddistance = L.index(distance)
                city = cityList[inddistance]
                list_of_nearby_cities.append(city)
                L[inddistance] = 0
        i = indcity + 1
        if i in range(len(distanceList)):
            while i < len(distanceList):
                index_value = i - indcity
                index_value -= 1
                if distanceList[i][index_value] <= r:
                    city = cityList[i]
                    list_of_nearby_cities.append(city)
                i += 1
        return list_of_nearby_cities


def numofcitiesserved(cityList, distanceList, name, r):
    served = [False] * 128
    for name in nearbyCities(cityList,distanceList,name, r):
        city_index = cityList.index(name)
        served[city_index] = True
    return served



def locateFacilities(cityList, distanceList, r):
    max_count = 0
    best_city_list = []
    for name in cityList:
        num_of_served = numofcitiesserved(cityList,distanceList, name, r).count(True)
        if num_of_served > max_count:
            max_count = num_of_served
            best_city_list += nearbyCities(cityList, distanceList, name, r)
    return best_city_list
