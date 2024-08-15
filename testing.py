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

# goal is to have every value in served to be True!!
# we have to figure out how many facilities to use aka, we return the cities where there are facilities
# so we need to pick ou the cities that serve the most amount of other cities.
# we need to sort these cities to view from max to min or min to max. ? Each city can be considered a facility.
# this is now a list [ c1, c2, c3, c4, c5, c6...] c1 is the city with most cities served
# now this is like the money problem.
# we need every value in served to be True
# how many true if we place a facility at c1? how many False's are left? At which cities?

#try next city. How many cities do they change to True? (they may service cities already TRUE, do not count those)
#make this the max_count
# make the served list == to only the Trues that exist again after placing a facilitiy at c1
#try next city. How many cities do they change to True?
#make this the max count.
# go through every city.
#find the city that changes the most False to True. Mark that city.
#update the list of served to equal both c1 and ci served cities.
#loop through every city after that city.
#update once found the best city.
#loop through the rest of the cities.
#keep updating.
#loop ends when every value of served is true
#return the cities that were marked

# 1. create a function that updates the served list according to the city.
# 2. create a function that counts the number of Trues in served list according to the city and
     # puts the cities in decreasing order of the number of Trues they have.




def citiesserved(cityList, distanceList, name, r):
    served = [False] * 128
    a = nearbyCities(cityList,distanceList, name, r)
    for name in a:
        city_index = cityList.index(name)
        served[city_index] = True
    return served

def updatebool_list (cityList, distanceList, name2, r, bool_list):
    name = name2
    norm_list = citiesserved(cityList, distanceList, name, r,)
    for value1 in bool_list:
        for value2 in norm_list:
            if value1 == False and value2 == True:
                #turn value1 into True
                ind = bool_list.index(value1)
                bool_list[ind] = 0
    return bool_list

def sorted_num_of_Trues_for_facility_city(cityList, distanceList, r):
    best_cities_to_served = [] #each with a nested list of [int(count), "name"]
    for name in cityList:
        nestedlist = []
        count = citiesserved(cityList, distanceList, name, r).count(True)
        nestedlist = [int(count), name]
        best_cities_to_served.append(nestedlist)
    answer = sorted(best_cities_to_served)
    answer = answer[::-1]
    return answer


# def locatefacilities(cityList, distanceList, r):
#     served = [False] * 128
#     facilities = []
#     while False in served:
#         best = 0
#         best_city = ""
#         for i in range(len(cityList)):
#             if served[i] == True:
#                 continue
#             if served[i] == False:
#                 name = cityList[i]
#                 temp_count = citiesserved(cityList, distanceList, name, r ).count(True)
#                 if temp_count > best:
#                     best = temp_count
#                     best_city = name
#
#
#     return facilities
#
#
# def locateFacilities(cityList, distanceList, r):
#     i = 0
#     facility_count = 0
#     least_facility_amount = 128
#     sorted_list = sorted_num_of_Trues_for_facility_city(cityList,distanceList,r)
#     while i < len(sorted_list):
#         name = sorted_list[i][1]
#         city_facilities = [name]     #these will then need to be sorted according to the order they
#                                      #appear in cityList
#         bool_list = citiesserved(cityList,distanceList, name, r)
#         for value in bool_list:
#             if value == True:
#                 ind = bool_list.index(True)
#                 bool_list[ind] = 1
#                 cityList.remove(cityList[ind])
#         j = i + 1
#         while j < len(sorted_list) - 1:
#             while False in bool_list:
#                 max_count = 0
#                 name2 = sorted_list[j][1]
#                 temp_count = (updatebool_list(cityList, distanceList, name2, r, bool_list)).count(True)
#                 if temp_count > max_count:
#                     max_count = temp_count
#                     city_facilities.append(name2)
#                     bool_list = updatebool_list(cityList,distanceList, name2, r, bool_list)
#             j += 1
#         facility_count = len(city_facilities)
#         if facility_count < least_facility_amount:
#             least_facility_amount = facility_count
#         i += 1
#     final_list = []
#     for name in city_facilities:
#         index = cityList.index(name)
#         final_list.append(index)
#     final = final_list.sorted()
#     for value in final:
#         ind = final.index(value)
#         final[ind] = cityList[value]
#     return final






    # for name in cityList:
    #     first_served = citiesserved(cityList, distanceList, name, r)
    #     for value in first_served:
    #         if value == True:
    #             ind = int(first_served.index(value))
    #             first_served[ind] = 0
    #     facilities = [name]
    #     facil_count = 1
    #     cityList.remove(name)
    #     while False in
    #     for name in cityList:
    #         temp_served = citiesserved(cityList, distanceList, name, r)
    #         num_of_true = temp_served.count(True)
    #         if num_of_true > max_temp_bool:
    #             max_temp_bool = num_of_true
    #             facilities.append(name)
    #     for value in temp_served:
    #         if value == True:
    #             ind = int(first_served.index(value))
    #             temp_served[ind] = 0

















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



def citiesserved(cityList, distanceList, name, r):
    served = [False] * 128
    a = nearbyCities(cityList,distanceList, name, r)
    for name in a:
        city_index = cityList.index(name)
        served[city_index] = True
    return served


def locatefacilities(cityList, distanceList,r):
    best_count = 0
    best_city = ""
    for name in cityList:
        bool_list = citiesserved(cityList,distanceList, name, r)
        temp_count = bool_list.count(True)
        if temp_count > max_count:
            max_count = temp_count
            best_city = name
    name = cityList.index(best_city)
    already_served = citiesserved(cityList, distanceList, name, r)
    cityList.remove(name)
    facilities = [name]
    while False in already_served:
        best = 0
        next_best_city = ""
        for i in range(len(cityList)):
            name = cityList[i]
            temp_served = citiesserved(cityList,distanceList,name, r)
            count = 0
            for j in range(len(temp_served)):
                if temp_served[j] == already_served[j]:
                    continue
                elif temp_served[j] == True and already_served[j] == False:
                    count += 1
            if count > best:
                best = count
                next_best_city = name
        facilities.append(name)



#make a function to remove cities already served?

def removeserved(served, cityList):



