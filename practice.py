s = [[10, "hi"], [2, "bye"], [0, "go"], [1, "bro"]]
count = [10,2,0,1]
cities = ["hi", "bye", "go", "bro"]
answer = sorted(count)
print(s.sort())
print(s)
print(count.sort())
print(cities.sort())
print(answer)
print(answer[::-1])
tri = sorted(s)
print(tri)
print(tri[::-1])

s = [True, True, False]
print(bool(s))
print(s)
if False in s:
    print("keep going")


for value in s:
    if value == True:
        ind = s.index(value)
        s[ind] = 0

print(s)
iowa_city = [True, False, False, True] # 2 true
moline = [False, False, True, True]  #2 true
rock_island = [False,True, True, True]  #three true
dubuque = [True, True, False, False]    # 2 true

# greedy will take rock_island first
#now, we can say :
bool_list = [False, 0, 0, 0]

# def updatebool_list (cityList, distanceList, name, r, bool_list):
#     norm_list = citiesserved(cityList, distanceList, name, r,)
#     temp_count = 0
#     for value1 in bool_list:
#         for value2 in norm_list:
#             if value1 == False and value2 == True:
#                 #turn value1 into True
#                 ind = bool_list.index(value1)
#                 bool_list[ind] = 0
#                 temp_count += 1
#     return temp_count


#we go through and see if any falses are turned True.
#write a program for that.

s = [True, 0, True, True]
print(s.count(True))

s = [False]
x = []

if False in x:
    print("hi")
if False in s:
    print("bye")
