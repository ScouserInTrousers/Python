#!/usr/bin/python
#Some fun with properties of the primes using only base Python

class Integer(object):
    _factorization = None
    _num_divisors = None

    def __init__(self, num):
        # self.word = word
        self.num = num
        self.nearest_prime = self.nearest_prime()
        self.primality = "Prime" if self.is_prime() else "Composite"
    
    def __repr__(self):
        return 'Integer({!r})'.format(self.num)

    def __add__(self,other):
        num = self.num + other.num
        return Integer(num)

    def __mul__(self,other):
        try:
            num = self.num * other.num
        except AttributeError:
            num = self.num * other

        return Integer(num)

    # @property
    # def primality(self):
    #     return self._primality

    @property
    def factorization(self):
        if self._factorization is None:
            self._factorization =' * '.join([str(k)+'^'+str(v) for k,v in 
               self.decompose().iteritems()]) 
        return self._factorization

    @property
    def num_divisors(self):
        """Returns the number of divisors of n. The Fundamental Theorem of 
        Arithmetic guarantees that every given integer is a unique product of
        powers of primes; i.e. for all z in Z, z = (p_1 ^ a_1 )*...*(p_n ^ a_n)
        for primes p_1, ..., p_n and integer powers a_1, ..., a_n. Moreover, 
        there is a theorem that states that the number of factors of a given 
        integer is equal to d(Z) = (a_1 + 1)*...*(a_n + 1). This function is an
        implementation of that theorem. More info at https://oeis.org/A000005"""

        if self._num_divisors is None:
            if self.num == 1: 
                self._num_divisors = 1
                return self._num_divisors
            else:
                self._num_divisors = reduce(lambda x,y:x*y, 
                    [z+1 for z in self.decompose().values()])
        return self._num_divisors

    def decompose(self):
        """Returns the dictionary of prime factors of the given integer, in the 
        form of "prime: power". Credit for the implementation must go to the 
        author: http://stackoverflow.com/a/412942/4747798"""
        
        z = self.num

        factors = []
        d=2
        while z > 1:
            while z % d == 0:
                factors.append(d)
                z /= d
            d = d + 1
            if d*d > z:
                if z > 1: factors.append(z)
                break

        return {f:factors.count(f) for f in set(factors)}

    def euler_totient(self):
        #TODO: Implement Euler's totient function; i.e. the count of integers
        #between 1 and z that are relatively prime to z
        z = self.num
        count = 0
        # for x in range(1,z+1):
        #     if 
        pass

    def gcd(self):
        #TODO: Implement greatest common divisor function as class method in 
        #order to facilitate other functions.
        pass

    def is_prime(self):
        """Takes an integer, z, and returns whether that integer is prime. This
        particular implementation inspired by 
        https://pythonism.wordpress.com/2008/05/04/looking-at-prime-numbers-in-python
        """

        z = self.num
    
        if z==1:
            return False

        if z % 2 == 0 and z != 2 or z % 3 == 0 and z != 3:
            return False
        
        for x in range(1, int( (z**0.5+1)/6.0 + 1 )):
            if z % (6*x - 1) == 0 or z % (6*x + 1) == 0:
                return False
        return True

    def nearest_prime(self):
        """This function finds the nearest prime number to integer input z"""
        z = self.num
        
        if z == 1: return 2
        if is_prime(z): return z

        first_before_z = [x for i,x in enumerate(range(z-1,1,-1)) if is_prime(x)==True][0]
        first_after_z = z+1
        while not is_prime(first_after_z):
            first_after_z +=1

        if cmp(abs(first_before_z - z), abs(first_after_z - z)) < 0:
            return first_before_z
        elif cmp(abs(first_before_z - z), abs(first_after_z - z)) > 0:
            return first_after_z
        else: 
            return (first_before_z, first_after_z)

    def pi(self):
        """This is an implementation of the Prime Counting Function, i.e. the 
        amount of primes not exceeding X."""
        
        z = self.num 
        return len( [x for x in range(1,z+1) if is_prime(x)] )

def decompose_integer(z):
    """Returns the dictionary of prime factors of the given integer, in the 
    form of "prime: power". Credit for the implementation must go to the 
    author: http://stackoverflow.com/a/412942/4747798"""
    
    assert type(z) == int

    factors = []
    d=2
    while z > 1:
        while z % d == 0:
            factors.append(d)
            z /= d
        d = d + 1
        if d*d > z:
            if z > 1: factors.append(z)
            break

    return {f:factors.count(f) for f in set(factors)}
    #sanity check: reduce(lambda x,y: x*y, map(pow, a.keys(),a.values())) == z

def is_prime(z):
    """Takes an integer, z, and returns whether that integer is prime. This
    particular implementation inspired by 
    https://pythonism.wordpress.com/2008/05/04/looking-at-prime-numbers-in-python
    """

    # assert type(z) == int;
    
    if z==1:
        return False

    if z % 2 == 0 and z != 2 or z % 3 == 0 and z != 3:
        return False
    
    for x in range(1, int( (z**0.5 + 1)/6.0 + 1 )):
        if z % (6*x - 1) == 0 or z % (6*x + 1) == 0:
            return False

    return True

def nearest_prime(z):
    """This function finds the nearest prime number to integer input z"""
    assert type(z) == int

    if z == 1:
        print 'The nearest prime is 2'
        return
    if is_prime(z): 
        print 'The nearest prime is %d' % z
        return

    first_before_z = [x for i,x in enumerate(range(z-1,1,-1)) if is_prime(x)==True][0]
    first_after_z = z+1
    while not is_prime(first_after_z):
        first_after_z +=1

    if cmp(abs(first_before_z - z), abs(first_after_z - z)) < 0:
        print 'The nearest prime, {0}, is only {1} integers away.'.format(
        first_before_z, abs(first_before_z - z) )
        return
    elif cmp(abs(first_before_z - z), abs(first_after_z - z)) > 0:
        print 'The nearest prime, {0}, is only {1} integers away.'.format( 
        first_after_z, abs(first_after_z - z))
        return
    else:
        print 'Whoa, this is neat! There are two primes that are nearest to \
                %d: %d and %d! Nobody knows if this happens infinitely often:\
                see http://math.stackexchange.com/a/82668 \
                for more details!'  % (z, first_before_z, first_after_z)
        return

def nth_most_divisors(n):
    """This function returns the nth highly composite number; i.e. natural 
    number with nth most divisors. E.g. 1 is the 1st HCN because no natural
    number has more factors; 2 is the second HCN because it has the most 
    factors of all natural numbers less than or equal to 2. More info at 
    https://oeis.org/A002182"""
    
    assert type(n) == int
    assert n > 0

    if(n==1):
        return 1
    record = [1]
    z=2

    while z >= 1:
        # Get the number of divisors of the current integer
        dz = d(z)
        # Main logic of the program
        if dz > max(record):
            record.append(dz)
            if len(record) == n:
               break
            else:
                z+=1
                continue
        elif dz == max(record):
            z += 1
            continue
        else:
            z+=1
            continue

    return z

def pi(z):
    """This is an implementation of the Prime Counting Function, i.e. the 
    amount of primes not exceeding X."""
    
    assert type(z) == int
    return len( [x for x in range(1,z+1) if is_prime(x)] )
    #Possible speed up: return sum(map(is_prime, range(1,z+2)))

def text2int(textnum, numwords={}):
    if not numwords:
        units = [ "zero", "one", "two", "three", "four", "five", "six", 
                "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen"
                , "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", 
                "nineteen"]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", 
                "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]

    numwords["and"] = (1, 0)
    for idx, word in enumerate(units):    
        numwords[word] = (1, idx)
    for idx, word in enumerate(tens):     
        numwords[word] = (1, idx * 10)
    for idx, word in enumerate(scales):   
        numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current
#Create a function that makes a call to OEIS and returns the URLs of the sequences in which#a given integer appears. Also, want to implement an antiprimes function i.e. the
#Numberphile post about the nth most composite number 
