#!/usr/bin/python
#The purpose of this script is to give my intution about primes

def isPrime(X, naive=True):
    """Takes an integer, x, and returns whether that integer is prime"""
    
    #Error checking of the input
    assert type(X) == int;
   
    #Special case of the input:
    if X ==1: print 'False. 1 is not prime because the Fundamental Theorem of Arithmetic says so!'; return
    
    #Logic of the function 
    if X%2==0 and X!=2 or X%3==0 and X!=3:
        return False
    for z in range(1, int((X**0.5+1)/6 + 1 )):
        if X % (6*z-1) == 0 or X % (6*z+1) == 0:
            return False
    return True

def nearestPrime(X):
    """If X is returned as not prime via primeFinder.isPrime, this function finds the nearest prime number to it"""

    if X == 1: print 'The nearest prime is 2';return
    if isPrime(X): print 'The nearest prime is %d' % X; return 
    first_prime_before_x = [z for i,z in enumerate(range(X-1,1,-1)) if isPrime(z)==True][0]
    first_prime_after_x = X+1
    while isPrime(first_prime_after_x) == False:
        first_prime_after_x +=1

    if cmp(abs(first_prime_before_x - X), abs(first_prime_after_x - X)) < 0:
        print 'The nearest prime, %d, is only %d integers away.' % (first_prime_before_x, abs(first_prime_before_x - X))
        return
    elif cmp(abs(first_prime_before_x - X), abs(first_prime_after_x - X)) > 0:
        print 'The nearest prime, %d, is only %d integers away.' % (first_prime_after_x, abs(first_prime_after_x - X))
        return
    else:
        print 'Whoa, this is neat! There are two primes that are nearest to %d: %d and %d! Nobody knows if this happens infinitely often: see http://math.stackexchange.com/a/82668 for more details!' % (X, first_prime_before_x, first_prime_after_x)
        return

def decomposeInteger(X, FToA = False):
    """Returns the tuple of prime factors of the given integer. Credit for this implementation must go to the author: http://stackoverflow.com/a/412942/4747798"""
    assert type(X) == int
    if isPrime(X): return (1, X)
    factors = []
    d=2
    while X > 1:
        while X % d == 0:
            factors.append(d)
            X /= d
        d = d + 1
        if d*d > X:
            if X > 1: factors.append(X)
            break
    if not FToA: return tuple(factors)
    else: return {f:factors.count(f) for f in set(factors)}
    #sanity check: reduce(lambda x,y: x*y, map(pow, a.keys(),a.values()))i == X


def pi(X):
    """This is an implementation of the Prime Counting Function, i.e. the amount of primes not exceeding X."""
    assert type(X) == int
    if isPrime(X): return 1
    return len(decomposeInteger(X,True).keys())

def antiPrime(n):
    """This function returns the nth antiprime, i.e. the smallest composite integer with n prime factors. """
What I want to be able to make is a function that returns tuples of the prime
#factors and the powers on the primes, so that I can move forward with all the
#fun theorems. Also, want to implement an antiprimes function i.e. the Numberphile
#post about the nth most composite number 
