#!/usr/bin/python
#Ixnay on the import statements!

class Integer(object):

    def __init__(self, num):
        self.num = num
    
    def __repr__(self):
        return 'Integer({!r})'.format(self.num)

    def __add__(self,other):
        try:
            num = self.num + other.num
        except AttributeError:
            num = self.num + other

        return Integer(num)

    def __mul__(self, other):
        try:
            num = self.num * other.num
        except AttributeError:
            num = self.num * other

        return Integer(num)

    def __pow__(self, p):
        num = self.num ** p
        
        return Integer(num)

    def __lt__(self, other):
        return self.num < other

    def __le__(self, other):
        return self.num <= other

    def __gt__(self, other):
        return self.num > other

    def __ge__(self, other):
        return self.num >= other

    def is_perfect_k(self, k):
        """Returns whether the Integer is a perfect k-power e.g. square (k=2),
        cube (k=3), etc.
        """
        return all(x % k==0 for x in self.decomposition.itervalues())

    @staticmethod
    def gcd(a, b):
        """Greatest common divisor of two integers is the integer n that
        satisfies max({n: a%n=0 & b%n=0, n <= a <= b})
        """
        #Note: could also frame this as set intersection of divisors of a,b
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def is_prime(z):
        """Takes an integer, z, and returns whether that integer is prime. This
        particular implementation inspired by 
        http://web.archive.org/web/20170108014244/https://pythonism.wordpress\
        .com/2008/05/04/looking-at-prime-numbers-in-python/
        """

        if z==1 or z % 2 == 0 and z != 2 or z % 3 == 0 and z != 3:
            return False
        
        for x in range(1, int( (z**0.5 + 1)/6.0 + 1 )):
            if z % (6*x - 1) == 0 or z % (6*x + 1) == 0:
                return False

        return True
	
    #A clever implementation from SO:
	#http://stackoverflow.com/a/27946768
	# def is_prime(z):
	# 	return n > 1 and all(n % k for k in xrange(2, int(n**0.5 + 1))
	
    @property
    def binary(self):
        """Return Python binary of the integer
        """
        return bin(self.num)

    @property
    def decomposition(self):
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

    @property
    def divisors(self):
        """Returns the set of divisors
        """
        return set(k**x for k,v in self.decomposition.iteritems()
                        for x in range(0,v+1) if k**x <= k**v)

    @property
    def euler_totient(self):
        """phi(z) = count of integers <= z coprime to z 
        """
        return len(self.totatives)

    @property
    def factorization(self):
        """Quasi human-readable rendering of prime decomposition
        """
        return ' * '.join([str(k)+'^'+str(v) for k,v in 
                           self.decomposition.iteritems()]) 

    @property
    def nearest_prime(self):
        """This function finds the nearest prime number to integer input z"""

        z = self.num
        if z in (0, 1): return 2
        if self.is_prime(z): return z

        #It is probably in violation of D.R.Y. to have these two generators
        #be so similar yet separate. Refactoring seems that it would add
        #complexity just for style points, however

        #Generator to get the first prime before z
        def before(z):
            i = z - 1
            while True:
                if self.is_prime(i):
                    yield i
                else:
                    i -= 1
                    continue

        #Generator to get the first prime after z
        def after(z):
            i = z + 1
            while True:
                if self.is_prime(i):
                    yield i
                else:
                    i += 1
                    continue

        first_before_z = before(z).next()
        first_after_z = after(z).next()

        if abs(first_before_z - z) < abs(first_after_z - z):
            return first_before_z
        if abs(first_before_z - z) > abs(first_after_z - z):
            return first_after_z
        else: 
            return (first_before_z, first_after_z)

    @property
    def num_divisors(self):
        """Returns the number of divisors of n. The Fundamental Theorem of 
        Arithmetic guarantees that every given integer is a unique product of
        powers of primes; i.e. for all z in Z, z = (p_1 ^ a_1 )*...*(p_n ^ a_n)
        for primes p_1, ..., p_n and integer powers a_1, ..., a_n. Moreover, 
        there is a theorem that states that the number of factors of a given 
        integer is equal to d(Z) = (a_1 + 1)*...*(a_n + 1). This function is an
        implementation of the theorem. More info at https://oeis.org/A000005"""

        if self.num == 1: 
            return 1
        else:
            return reduce(lambda x,y:x*y, 
                [z+1 for z in self.decomposition.values()])

    @property
    def Omega(self):
        """The total number of prime factors of n
        """
        return sum(self.decomposition.itervalues())

    @property
    def omega(self):
        """The number of distinct prime factors of n
        """
        return len(self.decomposition)

    @property
    def pi(self):
        """Prime Counting Function, i.e. the amount of primes not exceeding
        Integer."""
        #TODO: refactor this as a generator, with a producer and consumer
        z = self.num 
        return len([x for x in range(1,z+1) if self.is_prime(x)])

    @property
    def primality(self):
        """"Prime" if prime, "Composite" if not
        """
        return "Prime" if self.is_prime(self.num) else "Composite"
    
    @property
    def totatives(self):
        """The totatives of z are the k in Z, 1<=k<=z, that are coprime to z
        """
        z = self.num
        return set([x for x in range(1, z+1) if self.gcd(z, x) == 1])

    # def is_prime(self):
    #     """Takes an integer, z, and returns whether that integer is prime. This
    #     particular implementation inspired by 
    #     http://web.archive.org/web/20170108014244/https://pythonism.wordpress\
    #     .com/2008/05/04/looking-at-prime-numbers-in-python/
    #     """
    #     z = self.num
    
    #     if z in (0, 1):
    #         return False

    #     if z % 2 == 0 and z != 2 or z % 3 == 0 and z != 3:
    #         return False
        
    #     for x in range(1, int( (z**0.5+1)/6.0 + 1 )):
    #         if z % (6*x - 1) == 0 or z % (6*x + 1) == 0:
    #             return False
    #     return True


def eratosthenes():
	'''Yields the sequence of prime numbers via the Sieve of Eratosthenes.
        Courtesy of David Eppstein, UC Irvine, 28 Feb 2002
        http://code.activestate.com/recipes/117119/
        '''
	D = {}  # map composite integers to primes witnessing their compositeness
	q = 2   # first integer to test for primality
	while 1:
            if q not in D:
                yield q        # not marked composite, must be prime
                D[q*q] = [q]   # first multiple of q not already marked
            else:
                for p in D[q]: # move each witness to its next multiple
                    D.setdefault(p+q,[]).append(p)
                del D[q]       # no longer need D[q], free memory
            q += 1
	#Version suggested in the comments
	# while True:   
	#     p = D.pop(q, None)
	#     if p:
	# 	x = p + q
	# 	while x in D: x += p
	# 	D[x] = p   
	#     else:
	# 	D[q*q] = q
	# 	yield q
	#     q += 1

def nth_most_divisors(n):
    """This function returns the nth highly composite number; i.e. natural 
    number with nth most divisors. E.g. 1 is the 1st HCN because no natural
    number has more factors; 2 is the second HCN because it has the most 
    factors of all natural numbers less than or equal to 2. More info at 
    https://oeis.org/A002182"""
    
    if(n==1):
        return 1
    record = [1]
    z = 2

    while z >= 1:
        # Get the number of divisors of the current integer
        dz = len(Integer(z).divisors)
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

#Create a function that makes a call to OEIS and returns the URLs of the sequences in which#a given integer appears. Also, want to implement an antiprimes function i.e. the
#Numberphile post about the nth most composite number 


#TESTS:
#two = Integer(2)
#three = Integer(3)
#Integer.gcd(2,3) == max(two.divisors & three.divisors)

#twelve = Integer(12)
#twelve.num == [k**v for k,v in twelve.decomposition.iteritems()][0]
