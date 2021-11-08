

# Function to check whether the scoop is within the scoop Limit...
def scoopCheck(scoopLimit):
    flag = True
    while flag == True:
        scoopNumber = int(input("Enter the number of scoop to add:\n"))
        if scoopNumber <= scoopLimit:
            flag = False
        else:
            print("Maximum soop Limit is {}".format(scoopLimit))
    return scoopNumber

# Function to check whether the topping is within the topping Limit...
def toppingCheck(toppingLimit):
    flag = True
    while flag == True:
        toppingNumber = int(input("Enter the number of toppings to add:\n"))
        if toppingNumber <= toppingLimit:
            flag = False
        else:
            print("Maximum topping limit is {}".format(toppingLimit))
    return toppingNumber

# Function to get the user input and store it in the dictionary, returns dictionary...
def productCheck(coneNamePrice,scoopFlavours,toppingNamePrice,scoopLimit,toppingLimit):
    flag1 = True
    flag2 = True
    flag3 = True
    while flag1 == True:
        print("\n")
        print(coneNamePrice)
        coneType = str(input("Enter the choice of cone for icecream {}\n".format(i+1)))
        if coneType not in coneNamePrice.keys(): # prompting the user to input if the given input is not found in the dictionary...
            print("please select from options above")
        else:
            # getting the number of occurences of the user input
            if coneType not in qtyDict.keys(): 
                qtyDict[coneType] = 1
            else:
                qtyDict[coneType] += 1
            flag1 = False
    while flag2 == True:
        print("\n")
        print(scoopFlavours)
        flavour = str(input("Enter the flavour for icecream {}\n".format(i+1)))
        if flavour not in scoopFlavours:
            print("please select from options above")
        else:
            scoopNumber = scoopCheck(scoopLimit)
            if flavour not in qtyDict.keys():
                qtyDict[flavour] = 1*scoopNumber
            else:
                qtyDict[flavour] += 1*scoopNumber
            flag2 = False
    while flag3 == True:
        print("\n")
        print(toppingNamePrice)
        topping = str(input("Enter the topping for icecream {}\n".format(i+1)))
        if topping not in toppingNamePrice.keys():
            print("please select from options above")
        else:
            toppingNumber = toppingCheck(toppingLimit)
            if topping not in qtyDict.keys():
                qtyDict[topping] = 1*toppingNumber
            else:
                qtyDict[topping] += 1*toppingNumber
            flag3 = False
    return qtyDict
        

# main program...
coneNamePrice = {"plain cone":1.5,"waffle cone":2,"cup":1}
scoopFlavours = ["vanilla","strawberry","chocolate","caramel","mint","rainbow","coffee","bubble gum"]
scoopNamePrice = {scoopFlavours[i]:0.5 for i in range(len(scoopFlavours))}
toppingNamePrice = {"peanuts":0.75,"caramel sauce":0.5,"rainbow sprinkles":0.5,"pecan":1,"chocolate sprinkles":0.5}
rateList = {**coneNamePrice,**scoopNamePrice,**toppingNamePrice} # concatenating the dictionary...
scoopLimit = 3
toppingLimit = 4

customerName = str(input("Enter your name:\n")).upper()
print("\n")
print("Welcome {}".format(customerName))
numIcecream = int(input("Enter the number of icecreams\n"))
qtyDict = {}
for i in range(numIcecream):
    qtyDict = productCheck(coneNamePrice,scoopFlavours,toppingNamePrice,scoopLimit,toppingLimit)

print("S.no\tItem\t\t\t\tQuantity\t\t\tRate\t\t\tAmount")
sum = 0
for i in range(len(qtyDict)):
    print("{}\t{:<20}\t\t{:<10}\t\t\t{}\t\t\t{}".format(i+1,list(qtyDict.keys())[i],list(qtyDict.values())[i],rateList[list(qtyDict.keys())[i]],list(qtyDict.values())[i]*rateList[list(qtyDict.keys())[i]]))
    sum += list(qtyDict.values())[i]*rateList[list(qtyDict.keys())[i]]
print("\n")
print("your total bill is {}".format(sum))
print("Thank you. Have a Nice Day!!!")
