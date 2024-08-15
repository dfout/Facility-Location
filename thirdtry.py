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


#
#
#
#
# def citiesServed(cityList, distanceList, name, r, served):
#     a = nearbyCities(cityList,distanceList, name, r)
#     city_index = cityList.index(name)
#     served[city_index] = True
#     for name in a:
#         city_index = cityList.index(name)
#         served[city_index] = True
#     return served
#
#
#
#
# def updateList(temp_served, unserved):
#     updated_served =[]
#     for value1 in temp_served:
#         for value2 in unserved:
#             if value1 == True and value2 == True:
#                 updated_served.append(True)
#             elif value2 == False and value1 == True:
#                 updated_served.append(True)
#             elif value1 == False and value2 == True:
#                 updated_served.append(True)    #had this as false
#             elif value1 == False and value2 == False:
#                 updated_served.append(False)
#     return updated_served
#
#
# def locateFacilities(cityList, distanceList, r):
#     served = [False] * len(cityList)
#     name = find_best_city_to_start(cityList, distanceList,r)
#     facilities = [name]
#     unserved = citiesServed(cityList, distanceList, name, r, served)
#     while False in unserved:
#         max_count = 0
#         best_city = ""
#         for name in cityList:
#             if name in facilities:
#                 continue
#             else:
#                 temp_served = citiesServed(cityList, distanceList, name, r, served)
#                 count = 0
#                 for value2 in temp_served:
#                     for value1 in unserved:
#                         if value2 == True and value1 == False:
#                             count +=1
#                 if count > max_count:
#                     max_count = count
#                     best_city = name
#         facilities.append(best_city)
#         name = best_city
#         temp_served = citiesServed(cityList, distanceList, name, r, served)
#         unserved = updateList(temp_served, served)
#     return facilities












# RETURNS ONLY A LIST OF FALSE VALUES
# def citiesUnserved(cityList,distanceList,name,r):
#     served = [False] * len(cityList)
#     a = nearbyCities(cityList,distanceList,name,r)
#     city_index = cityList.index(name)
#     served[city_index] = True         #will this be a problem if anything changes?
#     for name in a:
#         city_index = cityList.index(name)
#         served[city_index] = True
#     for value in served:
#         if value == True:
#             served.remove(value)
#     return served





# RETURNS THE FULL BOOLEAN LIST

#colin's:

# def option(cityList, distanceList, r):
#     first_city = find_best_city_to_start(cityList, distanceList, r)
#     unserved = []
#     facilities = []
#     while False in served:
#         best = 0
#         best_city = ""
#         for i in range(len(cityList)):
#             if served[i] == True:
#                 continue
#             if served[i] == False:
#                 unserved.append(served[i])
#     return facilities
#
#
#
#
#
#
#
# # RETURNS ONLY A LIST OF FALSE VALUES
# def citiesUnserved(cityList,distanceList,name,r):
#     served = [False] * len(cityList)
#     a = nearbyCities(cityList,distanceList,name,r)
#     city_index = cityList.index(name)
#     served[city_index] = True         #will this be a problem if anything changes?
#     for name in a:
#         city_index = cityList.index(name)
#         served[city_index] = True
#     for value in served:
#         if value == True:
#             served.remove(value)
#     return served
#
#
# #
# def citiesserved(cityList, distanceList, name, r): #this function should find the number of unserved
#     served = [False] * len(cityList)                         #cities within distance r of the city
#     a = nearbyCities(cityList,distanceList, name, r)
#     city_index = cityList.index(name)
#     served[city_index] = True
#     for name in a:
#         city_index = cityList.index(name)
#         served[city_index] = True
#     return served
#
# def find_best_city_to_start(cityList,distanceList, r):
#     best_amount_of_served = 0
#     best_city = ""
#     for name in cityList:
#         bool_list = citiesserved(cityList,distanceList,name, r)
#         temp_count = bool_list.count(True)
#         if temp_count > best_amount_of_served:
#             best_amount_of_served = temp_count
#             best_city = name
#     return best_city
#
#
#
#
#

#
#
#
#
#
#
# def removeserved(served):
#     for value in served:
#         if value == True:
#             served.remove(value)
#     return served
#
#
# def locateFacilities(cityList,distanceList,r):
#     sorted_list = sorted_num_of_Trues_for_facility_city(cityList, distanceList, r)
#     name = find_best_city_to_start(cityList, distanceList, r)
#     served = citiesserved(cityList, distanceList, name, r)
#     facilities = [name]
#     #unserved = removeserved(served, cityList)
#     # REMOVE THE BEST CITY AND ITS SERVED FROM THE LIST SO ONLY FALSE VALUES EXIST
#     i = 0
#     final_facilities = [0] * 128
#     while False in served:
#             for j in range(len(cityList)):
#                 best_count = 0
#                 best_city = ""
#                 for name in cityList:
#                     if name in facilities:
#                         continue
#                     elif name not in facilities:
#                         temp_served = citiesserved(cityList, distanceList, name, r)
#                         count = 0
#                         for value1 in temp_served:
#                             for value2 in served:
#                                 if value1 == True and value2 == False:
#                                     count += 1
#                         if count > best_count:
#                             best_count = count
#                             best_city = name
#                 facilities.append(best_city)
#                 name = best_city
#                 temp_served = citiesserved(cityList,distanceList,name,r)
#                 served = updatelist(temp_served, served)
#             if False in served:
#                 i += 1
#                 continue
#             elif len(facilities) < len(final_facilities):
#                 final_facilities = facilities
#     return final_facilities

def bool_list(cityList, distanceList, name, r):
    first_bool = [False] * 128
    L = nearbyCities(cityList, distanceList, name, r)
    city_index = cityList.index(name)
    first_bool[city_index] = True
    for name in L:
        ind = cityList.index(name)
        first_bool[ind] = True
    return first_bool

def sorted_num_of_Trues_for_facility_city(cityList, distanceList, r):
    best_cities_to_served = [] #each with a nested list of [int(count), "name"]
    for name in cityList:
        nestedlist = []
        served = bool_list(cityList, distanceList, name, r)
        count = served.count(True)
        nestedlist = [int(count), name]
        best_cities_to_served.append(nestedlist)
    answer = sorted(best_cities_to_served)
    answer = answer[::-1]
    return answer

# def find_best_city_to_start(cityList,distanceList, r):
#     best_amount_of_served = 0
#     best_city = ""
#     for name in cityList:
#         bool_list = citiesServed(cityList,distanceList,name, r, served)
#         temp_count = bool_list.count(True)
#         if temp_count > best_amount_of_served:
#             best_amount_of_served = temp_count
#             best_city = name
#     return best_city

def find_best_city(served, facilities, cityList, distanceList, r):
    best_served = 0
    best_city = ""
    for name in cityList:
        count = 0
        if name not in facilities:
            temp_served = bool_list(cityList, distanceList, name, r)
            for value1 in temp_served:
                for value2 in served:
                    if value1 == True and value2 == False:
                        count += 1
            if count > best_served:
                best_served = count
                best_city = name
    return best_city


def updateList(served, temp_bool):
    updated_served = []
    for value1 in temp_bool:
        for value2 in served:
            if value1 == True and value2 == True:
                updated_served.append(True)
            elif value2 == False and value1 == True:
                updated_served.append(True)
            elif value1 == False and value2 == True:
                updated_served.append(True)  # had this as false
            elif value1 == False and value2 == False:
                updated_served.append(False)
    return updated_served




def locateFacilities(cityList, distanceList, r):
    served = [False] * 128
    facilities = []
    while False in served:
        name = find_best_city(served, facilities, cityList, distanceList, r)
        temp_bool = bool_list(cityList, distanceList, name, r)
        served = updateList(served, temp_bool)
        facilities.append(name)
    return facilities


cityList = []
coordList = []
popList = []
distanceList = []

loadData(cityList, coordList, popList, distanceList)

print(locateFacilities(cityList, distanceList, 1000))