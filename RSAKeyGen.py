"""
Author  - Temo Meza
Course  - CSC-592-02
Date    - 12/15/2022
Purpose - RSA Key Generation Project
"""

import random

def euclidExtended(m, n):
    x = 0
    y = 0
    s1 = 1
    s2 = 0
    t1 = 0
    t2 = 1

    if n > m:
        x = n
        y = m
    else:
        x = m
        y = n

    r = 1
    count = 1
    print("%s%6s%6s%6s%6s%6s%6s" % ("i", "q", "ri", "ri+1", "ri+2", "s", "t"))
    while r != 0:
        r = x % y
        q = x // y

        temp = s2
        s2 = s1 - q * s2
        s1 = temp

        temp = t2
        t2 = t1 - q * t2
        t1 = temp

        print("%d%6d%6d%6d%6d%6d%6d" % (count, q, x, y, r, s1, t1))

        count += 1
        x = y
        y = r
    return [s1, t1, x]

def primalityTest(x, e, n):
    # Initialization
    mainTable = []
    y = x
    e = bin(e)

    trace = ("%s| %4s| %4s| %4s| %4s\n" % ("i", "xi", "z", "y", "y"))
    trace += ("%s| %4s| %4s| %4s| %4s\n" % (len(e) - 3, e[2], "1", "1", y))
    for i in range(3, len(e)):
        z = y
        y = y * y % n
        y1 = y

        if (y == 1) and (z != 1) and z != n - 1:
            result = str(n) + " is not prime (bad square root)\n"
            return [False, trace, result]

        if e[i] == "1":
            y2 = y * x % n
            y = y * x % n
        else:
            y2 = y
        trace += ("%s| %4s| %4s| %4s| %4s\n" % (len(e) - (i+1), e[i], z, y1, y2))

    if y != 1:
        result = str(n) + " is not prime (bad final value)\n"
        return [False, trace, result]
    else:
        result = str(n) + " is perhaps prime\n"
        return [True, trace, result]

def RSAGen():
    goAgain = True
    while goAgain:  # For the rare case not a single e has an inverse
        # Initializing Variables
        p = 0
        q = 0
        goodTrace = True
        badTrace = True
        show = True

        # Generating random bits
        while q == 0:
            passedTest = False
            myBit = ""
            for i in range(5):
                bit = ""
                for j in range(32):
                    bit += str(random.randint(0, 1))
                if show:
                    print("b_" + str(i) + "|" + bit + "|" + bit[-1])
                myBit += bit[-1]
            myBit = "1" + myBit + "1"
            myNum = int(myBit, 2)
            if show:
                print("Number|" + str(myNum) + "|" + 25 * "0" + myBit)
                print()
            show = False

            # Miller-Rabin Test begins
            for i in range(20):
                a = random.randint(2, myNum - 1)
                results = primalityTest(a, myNum - 1, myNum)
                if (badTrace) and (not results[0]):
                    print("P = " + str(myNum) + ", a = " + str(a))
                    print(results[1])
                    print(results[2])
                    badTrace = False
                    break
                if not results[0]:
                    break
                if (results[0]) and (i == 19):
                    passedTest = True
            if passedTest:
                if p == 0:
                    if goodTrace:
                        print("P = " + str(myNum) + ", a = " + str(a))
                        print(results[1])
                        print(results[2])
                        goodTrace = False
                    p = myNum
                elif (p != 0) and (p != myNum):
                    q = myNum
        # Test Ends

        # In case 2 primes were chosen before a non prime appeared
        if badTrace:
            results = primalityTest(48, 92, 93)
            print(results[2])
            print(results[1])

        print("prime numbers used: " + str(p) + " and " + str(q))
        print()

        # Finding Inverse
        n = p * q
        phiN = (p-1) * (q-1)
        found = False
        for i in range(50):
            e = 3 + 2 * i
            print("e = " + str(e))
            inverses = euclidExtended(e, phiN)
            print('Euclid\'s returned:', inverses)
            print('n =', n)
            print()
            if inverses[2] == 1:
                inverse = inverses[1]
                while inverse < 0:
                    inverse += n
                if ((inverse * e) % phiN) == 1:
                    d = inverse
                    found = True
            if found:
                goAgain = False
                break

    # Finalizing Results
    print("p = %d, q = %d, n = %d, e = %d, d = %d" % (p, q, n, e, d))
    binP = bin(p)[2:]
    binQ = bin(q)[2:]
    binN = bin(n)[2:]
    binE = bin(e)[2:]
    binD = bin(d)[2:]

    print("p = " + (32-len(binP))*"0" + binP)
    print("q = " + (32-len(binQ))*"0" + binQ)
    print("n = " + (32-len(binN))*"0" + binN)
    print("e = " + (32-len(binE))*"0" + binE)
    print("d = " + (32-len(binD))*"0" + binD)

RSAGen()
#print(euclidExtended(3, 10600))