from relayeight import relayeight
import time

re = relayeight()
i = 1
print("Alle aus")
re.set_all(0, 0)
print(str(re.get_all(0)))
time.sleep(2)

"""
while True:
    print("Schalte 1 und 2 ein...")
    re.set_one(0, 1, 1)
    re.set_one(0, 2, 1)
    re.set_one(0, 3, 1)
    re.set_one(0, 4, 1)
    re.set_one(0, 5, 1)
    re.set_one(0, 6, 1)
    re.set_one(0, 7, 1)
    re.set_one(0, 8, 1)
    time.sleep(2)
    print("Schalte 1 und 2 aus...")
    re.set_one(0, 1, 0)
    re.set_one(0, 2, 0)
    re.set_one(0, 3, 0)
    re.set_one(0, 4, 0)
    re.set_one(0, 5, 0)
    re.set_one(0, 6, 0)
    re.set_one(0, 7, 0)
    re.set_one(0, 8, 0)
    time.sleep(2)
    """

while True:
    counter=0
    while counter < 8:
        counter+=1
        print("Ein: " + str(counter))
        re.set_one(0, counter, 1)
        time.sleep(0.1)
        

    while counter >= 1:    
        print("Aus: " + str(counter))
        re.set_one(0, counter, 0)
        time.sleep(0.1)
        counter-=1


    print(str(re.get_all(0)))
