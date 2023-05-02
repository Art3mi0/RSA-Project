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


def power(x, y, p):
    # Initialize result
    res = 1

    # Update x if it is more than or
    # equal to p
    x = x % p
    while (y > 0):

        # If y is odd, multiply
        # x with result
        if (y & 1):
            res = (res * x) % p

        # y must be even now
        y = y >> 1  # y = y/2
        x = (x * x) % p

    return res


# This function is called
# for all k trials. It returns
# false if n is composite and
# returns false if n is
# probably prime. d is an odd
# number such that d*2<sup>r</sup> = n-1
# for some r >= 1
def miillerTest(d, n):
    # Pick a random number in [2..n-2]
    # Corner cases make sure that n > 4
    a = 4 + secrets.randbelow(n - 4)

    # Compute a^d % n
    x = power(a, d, n)

    if (x == 1) or (x == n - 1):
        return True

    # Keep squaring x while one
    # of the following doesn't
    # happen
    # (i) d does not reach n-1
    # (ii) (x^2) % n is not 1
    # (iii) (x^2) % n is not n-1
    while (d != n - 1):
        x = (x * x) % n
        d *= 2

        if (x == 1):
            return False
        if (x == n - 1):
            return True

    # Return composite
    return False


# It returns false if n is
# composite and returns true if n
# is probably prime. k is an
# input parameter that determines
# accuracy level. Higher value of
# k indicates more accuracy.
def isPrime(n, k):
    # Corner cases
    if (n <= 1) or (n == 4):
        return False
    if (n <= 3):
        return True

    # Find r such that n =
    # 2^d * r + 1 for some r >= 1
    d = n - 1
    while (d % 2 == 0):
        d //= 2

    # Iterate given number of 'k' times
    for i in range(k):
        if (miillerTest(d, n) == False):
            return False;

    return True;

def RSAGen(bits):
    goAgain = True
    while goAgain:  # For the extremely rare case not a single e has an inverse
        # Initializing Variables
        p = 0
        q = 0

        # Generating random bits
        while q == 0:
            passedTest = False
            myNum = secrets.randbits(bits)
            myNum1 = myNum - 1
            numTests = 1

            result = isPrime(myNum, numTests)
            if result:
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

count = 0
print("Bit # \t time")
for i in range(248, 1025):
    start = time.perf_counter()
    n, e, d = RSAGen(i)
    end = time.perf_counter()
    encrypt = FastExponentiationNoTables.expMod(69, e, n)
    decrypt = FastExponentiationNoTables.expMod(encrypt, d, n)
    if decrypt != 69:
        count += 1
    print(str(i) + "\t" + str(end - start))

print(count, "total number of bad keys")

# The average time to generate keys is 0.6556628711999991 with 0 bad keys in 1000 tries
# https://www.geeksforgeeks.org/primality-test-set-3-miller-rabin/