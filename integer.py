#!/usr/bin/python
# Ixnay on the import statements!


def is_prime(z):
    """Takes an integer, z, and returns whether that integer is prime. Thiis
    particular implementation inspired by
    http://web.archive.org/web/20170108014244/https://pythonism.wordpress\
    .com/2008/05/04/looking-at-prime-numbers-in-python/
    """

    if z == 1 or z % 2 == 0 and z != 2 or z % 3 == 0 and z != 3:
        return False

    for x in range(1, int((z ** 0.5 + 1) / 6.0 + 1)):
        if z % (6 * x - 1) == 0 or z % (6 * x + 1) == 0:
            return False

    return True

# A clever implementation from SO:
# http://stackoverflow.com/a/27946768
#  def is_prime(z):
#  	return n > 1 and all(n % k for k in xrange(2, int(n ** 0.5 + 1))


class Integer(object):

    def __init__(self, num):
        self.num = num

    def __repr__(self):
        return 'Integer({!r})'.format(self.num)

    def __add__(self, other):
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

    def __eq__(self, other):
        return self.num == other

    def __ne__(self, other):
        eq_result = self == other
        if eq_result is NotImplemented:
            return NotImplemented
        else:
            return not eq_result

    def is_perfect_power(self, k):
        """Returns whether the Integer is a perfect k-power e.g. square (k=2),
        cube (k=3), etc.
        """
        return all(x % k == 0 for x in self.decomposition.itervalues())

    def is_power_of(self, n):
        """Is the integer, z, a power of n? I.e. z is a power of n <==>
        z = n^k for some integers n,k. E.g. 8 is a power of 2 because 8 = 2^3
        """
        return self.decomposition.keys() == [n]

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
        if z == 0:
            return None

        factors = []
        d = 2
        while z > 1:
            while z % d == 0:
                factors.append(d)
                z /= d
            d = d + 1
            if d * d > z:
                if z > 1:
                    factors.append(z)
                break

        return {f: factors.count(f) for f in set(factors)}

    @property
    def divisors(self):
        """Returns the set of divisors
        """
        # This is a temporary solution to robustly returning the
        # divisors using a cross-product of the factorization
        return {x for x in xrange(1, self.num+1) if self.num % x == 0}

    @property
    def euler_totient(self):
        """phi(z) = count of integers <= z coprime to z
        """
        return len(self.totatives)

    @property
    def factorization(self):
        """Quasi human-readable rendering of prime decomposition
        """
        return ' * '.join([str(k) + '^' + str(v) for k, v in
                           self.decomposition.iteritems()])

    @property
    def is_mersenne(self):
        """A Mersenne number is an integer, M, such that M = 2^k - 1, for some
        integer k
        """
        return Integer(self.num + 1).is_power_of(2)

    @property
    def is_mersenne_prime(self):
        """A Mersenne prime is a prime, p, of the form p = 2^k - 1, where
        k is an integer
        """
        return is_prime(self.num) and self.is_mersenne

    @property
    def is_perfect(self):
        return self.sigma == 2 * self.num

    @property
    def is_woodall(self):
        """A Woodall number is an integer, W, of the form W = k*2^k - 1, where
        k is an integer
        """
        if self.num < 1:
            return False
        w = Integer(self.num + 1)
        try:
            return w.decomposition[2] * pow(2, w.decomposition[2]) == w
        except KeyError:
            return False

    @property
    def is_woodall_prime(self):
        """A Woodall prime is a prime, p, of the form p = n*2^n - 1, where
        n is an integer
        """
        return is_prime(self.num) and self.is_woodall

    @property
    def nearest_prime(self):
        """This function finds the nearest prime number to integer input z"""

        z = self.num
        if z in (0, 1):
            return 2
        if is_prime(z):
            return z

        # It is probably in violation of D.R.Y. to have these two generators
        # be so similar yet separate. Refactoring seems that it would add
        # complexity just for style points, however
        # TODO: generate tuple of steps away in both directions; subtract/add
        # and take the min of that to get nearest prime

        # Generator to get the first prime before z
        def before(z):
            i = z - 1
            while True:
                if is_prime(i):
                    yield i
                else:
                    i -= 1
                    continue

        # Generator to get the first prime after z
        def after(z):
            i = z + 1
            while True:
                if is_prime(i):
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
    def parity(self):
        """Return whether integer is even or odd
        """
        return 'Odd' if self.num % 2 else 'Even'

    @property
    def pi(self):
        """Prime Counting Function, i.e. the amount of primes not exceeding
        Integer."""
        # TODO: refactor this as a generator, with a producer and consumer
        z = self.num
        return len([x for x in range(1, z+1) if is_prime(x)])

    @property
    def primality(self):
        """"Prime" if prime, "Composite" if not
        """
        return "Prime" if is_prime(self.num) else "Composite"

    @property
    def sigma(self):
        """Returns the aliquot sum of Integer plus the Integer itself, thus the
        sum of the divisors of the integer
        """
        return sum(self.divisors)

    @property
    def tau(self):
        """Returns the number of divisors of n. The Fundamental Theorem of
        Arithmetic guarantees that every given integer is a unique product of
        powers of primes; i.e. for all z in Z, z = (p_1 ^ a_1 )*...*(p_n ^ a_n)
        for primes p_1, ..., p_n and integer powers a_1, ..., a_n. Moreover,
        there is a theorem that states that the number of factors of a given
        integer is equal to d(Z) = (a_1 + 1)*...*(a_n + 1). This function is an
        implementation of the theorem. More info at https://oeis.org/A000005"""

        if self.num == 1:
            return 1
        if self.num == 0:
            return 0
        else:
            return reduce(lambda x, y: x * y,
                          [z + 1 for z in self.decomposition.values()])

    @property
    def totatives(self):
        """The totatives of z are the k in Z, 1<=k<=z, that are coprime to z
        """
        z = self.num
        if z == 0:
            return None
        return set([x for x in range(1, z+1) if gcd(z, x) == 1])


def nth_most_divisors(n):
    """This function returns the nth highly composite number; i.e. natural
    number with nth most divisors. E.g. 1 is the 1st HCN because no natural
    number has more factors; 2 is the second HCN because it has the most
    factors of all natural numbers less than or equal to 2. More info at
    https://oeis.org/A002182
    """

    if(n == 1):
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
                z += 1
                continue
        elif dz == max(record):
            z += 1
            continue
        else:
            z += 1
            continue

    return z

# TODO:Create a function that makes a call to OEIS and returns the URLs of the
# sequences in which a given integer appears. Also, want to implement an
# antiprimes function i.e. the Numberphile post about the nth most
# composite number


def gcd(a, b):
    """Greatest common divisor of two integers is the integer n that
    satisfies max({n: a%n=0 & b%n=0, n <= a <= b})
    """
    # Note: could also frame this as set intersection of divisors of a,b
    while b:
        a, b = b, a % b
    return a

# TESTS:
# two = Integer(2)
# three = Integer(3)
# Integer.gcd(2,3) == max(two.divisors & three.divisors)

# twelve = Integer(12)
# twelve.num == [k**v for k,v in twelve.decomposition.iteritems()][0]
