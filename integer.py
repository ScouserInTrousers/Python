#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Ixnay the import statements!


def is_prime(z):
    """Takes an integer and returns whether that integer is prime. This
    particular implementation from http://stackoverflow.com/a/27946768
    Args:
        z (int): Integer the primality of which to ascertain
    Returns:
        (bool): Whether `z` is prime
    """
    if z <= 1:
        return False
    for n in range(2, int(z ** 0.5 + 1)):
        if not z % n:
            return False
    else:
        return True


def sequence():
    """ Generate the following sequence:
    0, 1, -2, 3, -4, 5, -6, 7, -8, ...
    """
    n = 1
    yield 0
    while True:
        yield n
        sign = -1 if n % 2 else 1
        n = sign * (abs(n) + 1)


def generate_primes():
    """ Sieve of Eratosthenes variation to generate primes
    """
    found = list()
    candidate = 2
    while True:
        if all(candidate % prime for prime in found):
            yield candidate
            found.append(candidate)
        candidate += 1


class Integer(int):
    """
    A Python object to represent an integer with a superset of the
    methods of built-in int created in base Python 3 i.e. without
    any modules imported.
    Integer behaves as `int` in regards to arithmetic for numeric
    types e.g.

    >>> Integer("7") + 0 == 7
    True

    >>> Integer(4) * 3 == 12
    True

    >>> Integer(0) - 1 == -1
    True

    >>> Integer(8.4) + 0 == 8
    True

    Integer boasts of other attributes such as primality,
    subtypes of primality (e.g. Mersenne), perfectness, power-of
    checking, factorization, totatives, Goldbach partition, and
    methods such as nearest_prime and factorial.
    Most of the attributes of Integer are properties because just
    as the mathematical concept of an integer has the property
    that it is either prime or not, Integer has the Boolean
    property `primality`.
    """

    def __init__(self, num):
        try:
            self.num = int(num)
        except (OverflowError, TypeError, ValueError):
            raise ValueError("Integer must be finite and numeric")

    def __repr__(self):
        return "Integer({!r})".format(self.num)

    def __bool__(self):
        return self.num.__bool__()

    def __add__(self, other):
        num = self.num + other
        return Integer(num) if isinstance(num, int) else num

    def __sub__(self, other):
        num = self.num - other
        return Integer(num) if isinstance(num, int) else num

    def __mod__(self, other):
        num = self.num % other
        return Integer(num) if isinstance(num, int) else num

    def __rmod__(self, other):
        num = other % self.num
        return Integer(num) if isinstance(num, int) else num

    def __neg__(self):
        num = -self.num
        return Integer(num)

    def __mul__(self, other):
        num = self.num * other
        return Integer(num) if isinstance(num, int) else num

    def __rmul__(self, other):
        num = other * self.num
        return Integer(num) if isinstance(num, int) else num

    def __truediv__(self, other):
        num = self.num / other
        return num

    def __rtruediv__(self, other):
        num = other / self.num
        return num

    def __floordiv__(self, other):
        num = self.num / other
        return num

    def __rfloordiv__(self, other):
        num = other / self.num
        return num

    def __pow__(self, p):
        num = self.num ** p
        return Integer(num) if isinstance(num, int) else num

    @staticmethod
    def gcd(a, b):
        """Greatest common divisor of two integers is the integer n that
        satisfies max({n: a%n=0 & b%n=0, n <= a <= b})
        Args:
            a (int): first integer to compare
            b (int): second integer to compare
        Returns:
            (int): the largest integer between (inclusive) `a` and `b`
                such that it divides `a` and `b`
        """
        while b:
            a, b = b, a % b
        return a

    def is_perfect_power(self, k):
        """Returns whether the Integer is a perfect k-power e.g. perfect
        square (k=2), perfect cube (k=3), etc. Is only defined for k > 0
        E.g. Integer(16).is_perfect_power(2) == True because 4**2 == 16

        Args:
            k (int): power to check; i.e. is Integer() ** 1/k an integer?
        Returns:
            (bool)
        """
        if k <= 0:
            raise ValueError("Perfect negative power is not defined")
        elif k == 1:
            return True  # Trivial
        if self.num == 0:
            return True  # zero to any k is zero

        return all(x % k == 0 for x in self.decomposition.values())

    def is_power_of(self, n):
        """Is the integer, z, a power of n? I.e. z is a power of n if and
        only if z = n**k for some integers n>0, k. For example, 8 is a
        power of 2 because 8 = 2**3. Only implemented for positive integers
        Args:
            n (int): positive integer to ascertain whether Integer() is a
                power of it
        Returns:
            (bool)
        """
        if self.num < 0:
            raise NotImplementedError
            # m = n
            # while abs(n) < abs(self.num):
            #     n *= m
            #     if n == self.num:
            #         return True
            # else:
            #     return False
        elif self.num == 0:
            return False  # No exponentiation can result in 0
        elif self.num == 1:
            return True  # 1 is the zero-power of any given n

        if n < 0:
            raise ValueError
        elif n == 0:
            # Already know that z != 0 because logic has gotten to this point
            # There is no other such integer that is a zero-power of anything
            return False
        elif n == 1:
            # Already know that z != 1 because logic has gotten to this point
            # There is no other integer such that is a power of 1
            return False

        return list(self.decomposition.keys()) == [n]

    @property
    def binary(self):
        """Return Python binary of the integer
        """
        return bin(self.num)

    @property
    def decomposition(self):
        """Returns the dictionary of prime factors of the given integer, in the
        form of "prime: power". Credit for the implementation must go to the
        author: http://stackoverflow.com/a/412942/4747798
        """

        z = self.num
        if z in (0, 1):
            return {}

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

        return {int(f): int(factors.count(f)) for f in set(factors)}

    @property
    def divisors(self):
        """Returns the set of proper divisors of Integer()
        """
        return {x for x in range(1, self.num // 2 + 1) if not self.num % x}

    @property
    def euler_totient(self):
        """Returns phi(z) = count of positive integers less than or equal to
        z that are coprime to z
        """
        return Integer(len(self.totatives))

    @property
    def factorial(self):
        if self.num < 0:
            raise ValueError("Factorial is not defined for negative integers")
        elif self.num == 0:
            return Integer(1)
        else:
            def factorial_(n):
                return 1 if n < 1 else n * factorial_(n-1)
            return Integer(factorial_(self.num))

    @property
    def factorization(self):
        """Quasi human-readable rendering of prime decomposition
        """
        return " * ".join((str(k) + "^" + str(v) for k, v in
                           self.decomposition.items()))

    @property
    def goldbach_partitions(self):
        """Returns the Goldbach partitions of Integer(); i.e. the
        expression of an even number as a sum of two primes
        """

        if self.parity == "Odd":
            return set()
        return set((p, self.num-p)
                   for p in range(2, self.num // 2 + 1)
                   if is_prime(p) and is_prime(self.num - p))
    
    @property
    def is_balanced_prime(self):
        """A balanced prime is a prime, p, that is the average of
        the preceding and succeeding primes. Equivalently, if P is
        the previous prime and N is the next prime, then, for p to
        be a balanced prime, |N-p| = |P-p|; i.e. they must be 
        equidistant from p
        """
        if self.primality == 'Composite':
            return False
        z = self.num

        preceding_prime_candidate, succeeding_prime_candidate = (z, z)

        preceding_prime_candidate -= 1
        while not is_prime(preceding_prime_candidate):
            preceding_prime_candidate -= 1
        else:
            preceding_prime = preceding_prime_candidate

        # Shortcut: instead of repeating the search for n \in N
        # that are greater than z, just check if the succeeding
        # prime is the same distance from z
        distance_from_z = z - preceding_prime
        return True if is_prime(z + distance_from_z) else False

    @property
    def is_cullen(self):
        """A Cullen number is a natural number, C, of the form C = k*2**k  + 1,
        where k is an integer
        """
        k = 1
        w = self.num - 1
        candidate = k*2**k
        while candidate <= w:
            if w == candidate:
                return True
            k += 1
            candidate = k*2**k
            continue
        else:
            return False

    @property
    def is_cullen_prime(self):
        """A Cullen prime is a prime, p of the form p = k*2**k + 1, where k is
        an integer
        """
        return is_prime(self.num) and self.is_cullen

    @property
    def is_mersenne(self):
        """A Mersenne number is an integer, M, such that M = 2^k - 1, for some
        integer k
        """
        return self.num > 0 and Integer(self.num + 1).is_power_of(2)

    @property
    def is_mersenne_prime(self):
        """A Mersenne prime is a prime, p, of the form p = 2^k - 1, where
        k is an integer
        """
        return self.num > 0 and is_prime(self.num) and self.is_mersenne

    @property
    def is_perfect(self):
        """A positive integer is perfect if it is equal to the sum of its
        proper divisors; for instance, 6 has divisors {1, 2, 3, 6} (of which
        {1, 2, 3} are the proper divisors) and 1 + 2 + 3 = 6
        """
        return self.sigma == 2 * self.num

    @property
    def is_squarefree(self):
        """A positive integer is squarefree if it is not divisible by
        a square greater than 1.
        """
        if self.num < 1:
            return False
        elif self.num == 1:
            return True
        return all(exponent < 2 for exponent in self.decomposition.values())

    @property
    def is_woodall(self):
        """A Woodall number is an integer, W, of the form W = k*2**k - 1, where
        k is an integer
        """
        if self.num < 1:
            return False
        w = self.num + 1

        def woodall(k, w=w):
            return k * 2 ** k == w
        range_of_k_to_check = range(1, 4) if self.num < 64 else \
            range(1, int(pow(w, 1/3)) + 1)
        return any(map(woodall, range_of_k_to_check))

    @property
    def is_woodall_prime(self):
        """A Woodall prime is a prime, p, of the form p = k*2**k - 1, where
        k is an integer
        """
        return is_prime(self.num) and self.is_woodall

    @property
    def nearest_prime(self):
        """If Integer() is prime, returns Integer().num. Otherwise, returns
        either the nearest prime, or the two nearest primes, if equidistant
        Returns:
            (tuple)
        """

        if self.num <= 1:
            return (2,)
        elif is_prime(self.num):
            return (self.num,)
        else:
            z, s = self.num, sequence()

        while not is_prime(z):
            z += next(s)
        else:
            nearest = z - self.num

        # Is there another prime equidistant?
        return (z,) if not is_prime(self.num - nearest) else \
            tuple(sorted(z, self.num - nearest))

    @property
    def Omega(self):
        """The total number of prime factors of Integer()
        """
        return sum(self.decomposition.values())

    @property
    def omega(self):
        """The number of distinct prime factors of Integer()
        """
        return len(self.decomposition)

    @property
    def parity(self):
        """Return whether integer is even or odd
        """
        return "Odd" if self.num % 2 else "Even"

    @property
    def pi(self):
        """Prime Counting Function, i.e. the amount of primes not exceeding
        Integer
        """
        z = self.num
        return Integer(sum(1 for x in range(2, z + 1) if is_prime(x)))

    @property
    def primality(self):
        """Returns "Prime" if prime, "Composite" if not
        """
        return "Prime" if is_prime(self.num) else "Composite"

    @property
    def radical(self):
        """Returns the product of the distinct primes dividing n
        """
        z = self.num
        if self.is_squarefree:
            return Integer(z)
        else:
            product = 1
            for prime_factor in self.decomposition.keys():
                product *= prime_factor
            return Integer(product)

    @property
    def sigma(self):
        """Returns the aliquot sum of Integer plus the Integer itself;
        i.e. the sum of the divisors of the integer
        """
        return Integer(sum(self.divisors))

    @property
    def tau(self):
        """Returns the number of divisors of Integer. The Fundamental Theorem of
        Arithmetic guarantees that every given integer is a unique product of
        powers of primes; i.e. for all z in Z, z = (p_1 ^ a_1 )*...*(p_n ^ a_n)
        for primes p_1, ..., p_n and integer powers a_1, ..., a_n. Moreover,
        the number of factors of a given integer is equal to
        d(Z) = (a_1 + 1)*...*(a_n + 1). This function is an implementation of
        the theorem. More info at https://oeis.org/A000005"""

        if self.num <= 0:
            return Integer(0)
        elif self.num == 1:
            return Integer(1)
        else:
            product = 1
            for z in self.decomposition.values():
                product *= (z+1)
            return Integer(product)

    @property
    def totatives(self):
        """The totatives of z are the k in Z, 1<=k<=z, that are coprime to z
        """
        z = self.num
        if z <= 0:
            return set()
        return {x for x in range(1, z+1) if self.gcd(z, x) == 1}


def nth_most_divisors(n):
    """This function returns the nth highly composite number; i.e. natural
    number with nth most divisors. E.g. 1 is the 1st HCN because no natural
    number has more factors; 2 is the second HCN because it has the most
    factors of all natural numbers less than or equal to 2. More info at
    https://oeis.org/A002182
    Args:
        n (int): The element in Highly Composite Numbers sequence to return
    Returns:
        (int): the integer in position `n` in the Highly Composite Numbers seq
    """

    if n == 1:
        return 1
    record = [1]
    z = 2

    while z >= 1:
        # Get the number of divisors of the current integer
        dz = Integer(z).tau

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
