import random

def expMod(x, e, n):
    # Initialization
    mainTable = []
    y = x
    e = bin(e)

    for i in range(3, len(e)):
        addToTable = True   # A check that prevents the final part of the table from being added twice
        table = []          # Making a list that will be added to another list for table construction
        table.append(e[i])
        table.append(str(y) + "^2 mod " + str(n) + " = " + str(y * y % n))
        y = y * y % n

        if e[i] == "1":
            table.append(str(x) + " X " + str(y) + " mod " + str(n) + " = " + str(y * x % n))
            y = y * x % n
            addToTable = False
            # print(y)
        if addToTable:
            table.append(y)
        mainTable.append(table)

    # Table construction part
    print("Function answer:", y)
    print("Table: ")
    count = 0
    print("%2d| %2s| %17s| %s" % (len(mainTable), e[2], "", x))
    for i in mainTable:
        count += 1
        print("%2d| %2s| %17s| %s" % (len(mainTable) - count, i[0], i[1], i[2]))

#expMod(17, 22, 21)

# Test I used to ensure my function worked
# It matches the python calculations
# for i in range(10):
#     x = random.randint(15, 50)
#     e = random.randint(15, 50)
#     n = random.randint(15, 50)
#     print("x =", x, "e =", e, "n =", n)
#     print("Calculated answer =", (x**e) % n)
#     expMod(x, e, n)
#     print()

#p = 71, q = 83, n = 5893, e = 17, d = 1013

expMod(69, 17, 5893)
expMod(704, 1013, 5893)