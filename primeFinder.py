#!/usr/bin/python
#The purpose of this script is to give my intution about primes

def isPrime(X, naive=True):
    """Takes an integer, x, and returns whether that integer is prime"""
    
    #Error checking of the input
    assert type(X) == int;

    #Special case of the input:
    if X ==1: return False

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

def decomposeInteger(X):
    """Returns the dictionary of prime factors of the given integer, in the form of "prime: power". Credit for the implementation must go to the author: http://stackoverflow.com/a/412942/4747798"""
    assert type(X) == int
    #if isPrime(X): return (1, X)
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
    return {f:factors.count(f) for f in set(factors)}
    #sanity check: reduce(lambda x,y: x*y, map(pow, a.keys(),a.values())) == X

def d(n):
    """Returns the number of divisors of n. The Fundamental Theorem of Arithmetic guarantees that
every given integer is a unique product of powers of primes; i.e. for all z in Z, 
z = (p_1 ^ a_1 )*...*(p_n ^ a_n) for primes p_1, ..., p_n and integer powers a_1, ..., a_n.
Moreover, there is a theorem that states that the number of factors of a given integer
is equal to d(Z) = (a_1 + 1)*...*(a_n + 1). This function is an implementation of that
theorem. More info at https://oeis.org/A000005"""
    assert type(n) == int
    return reduce( lambda x,y: x*y, [z+1 for z in decomposeInteger(n).values()])

def pi(X):
    """This is an implementation of the Prime Counting Function, i.e. the amount of primes not exceeding X."""
    assert type(X) == int
    if isPrime(X): return 1
    return len(decomposeInteger(X,True).keys())

def nthMostDivisors(n):
    """This function returns the nth highly composite number; i.e. composite integer
with nth most divisors. E.g. 1 is the 1st antiprime because no integer has more
factors; 2 is the second HCN because it has the most factors of all integers less
than or equal to 2. More info at https://oeis.org/A002182"""
    assert type(n) == int
    if(n==1): return 1
    integer = 1
    num_factors = d(n)
#    while integer <= max_hcn:
#        if d(integer) == 2: integer+=1;continue
        
    #search_range = [z for z in range(1,n) if isPrime(z)==False]
#Create a function that makes a call to OEIS and returns the URLs of the sequences in which
#a given integer appears. Also, want to implement an antiprimes function i.e. the
#Numberphile post about the nth most composite number 
