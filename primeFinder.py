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
