#!/usr/bin/python
#The purpose of this script is to give my intution about primes

def isPrime(X, naive=True):
    """Takes an integer, x, and returns whether that integer is prime"""
    
    #Error checking of the input
    assert type(X) == int;
    if X==1: print '1 is not prime because the Fundamental Theorem of Arithmetic says so'; return
    
    #Naive method of searching for primes: is x mod z == 0 for 2 <= z < x?
    if naive:
        return not any( [X % z == 0 for z in range(2,X)] )
    else:
        #First check: parity --- if X even, return False
        if (X % 2 == 0) | (X % 5 == 0):
            return False
        #Sieve of Erostothenes, kind of: check the remainder of only the 
        #integers up to X that end in 1,3,7, or 9 
        else:
           return any( [17 % p for p in  [z for i,z in enumerate(range(2,X)) if (( X % 5 != 0) & (X % 2 != 0))] ] )

