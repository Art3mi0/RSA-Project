"""
Author  - Temo Meza
Course  - CSC-592-02
Date    - 12/15/2022
Purpose - RSA Key Generation Project
"""

import random
import secrets
import time

import FastExponentiationNoTables


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
    while r != 0:
        r = x % y
        q = x // y

        temp = s2
        s2 = s1 - q * s2
        s1 = temp

        temp = t2
        t2 = t1 - q * t2
        t1 = temp

        x = y
        y = r
    return t1, x

def primalityTest(x, e, n):
    # Initialization
    y = x
    e = bin(e)
    for i in range(3, len(e)):
        z = y
        y = y * y % n
        y1 = y

        if (y == 1) and (z != 1) and z != n - 1:
            return False

        if e[i] == "1":
            y2 = y * x % n
            y = y * x % n
        else:
            y2 = y

    if y != 1:
        return False
    else:
        return True

def RSAGen():
    goAgain = True
    while goAgain:  # For the extremely rare case not a single e has an inverse
        # Initializing Variables
        p = 0
        q = 0

        # Generating random bits
        while q == 0:
            passedTest = False
            myNum = secrets.randbits(512)
            myNum1 = myNum - 1
            numTests = 1

            # Miller-Rabin Test begins
            for i in range(numTests):  # was 20
                a = random.randint(2, myNum1)
                result = primalityTest(a, myNum1, myNum)
                if (result) and (i == numTests - 1):
                    passedTest = True
            if passedTest:
                if p == 0:
                    p = myNum
                elif (p != 0) and (p != myNum):
                    q = myNum
        # Test Ends

        # Finding Inverse
        n = p * q
        phiN = (p-1) * (q-1)
        found = False
        for i in range(50):
            e = 3 + 2 * i
            t1, x = euclidExtended(e, phiN)
            if x == 1:
                while t1 < 0:
                    t1 += n
                if ((t1 * e) % phiN) == 1:
                    d = t1
                    found = True
            if found:
                goAgain = False
                break

    return n, e, d
    # Finalizing Results
    # print("p = %d, q = %d, n = %d, e = %d, d = %d" % (p, q, n, e, d))
    # binP = bin(p)[2:]
    # binQ = bin(q)[2:]
    # binN = bin(n)[2:]
    # binE = bin(e)[2:]
    # binD = bin(d)[2:]
    #
    # print("p = " + (32-len(binP))*"0" + binP)
    # print("q = " + (32-len(binQ))*"0" + binQ)
    # print("n = " + (32-len(binN))*"0" + binN)
    # print("e = " + (32-len(binE))*"0" + binE)
    # print("d = " + (32-len(binD))*"0" + binD)

for i in range(50):
    sentence = "Attempt " + str(i + 1) + ": "
    start = time.perf_counter()
    n, e, d = RSAGen()
    end = time.perf_counter()
    print(sentence + str(end - start))
    encrypt = FastExponentiationNoTables.expMod(69, e, n)
    decrypt = FastExponentiationNoTables.expMod(encrypt, d, n)
    if decrypt != 69:
        print("Failed to properly decrypt \n")
    else:
        print("Properly decrypted \n")
