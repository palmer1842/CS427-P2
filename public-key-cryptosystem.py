def fast_exponent_mod(base, exponent, modulus):
    """
    An efficient implementation of fast exponentiation modulo n.

    This implementation comes from Introduction to Algorithms by Cormen, Leiserson, Rivest, Stein, as referenced in
    Professor Kabir's lecture notes.

    :param base: Integer - The base
    :param exponent: Integer - The exponent
    :param modulus: Integer - The modulus
    :return: Integer - The result of the exponentiation
    """

    c = 0
    d = 1
    binary_exp = format(exponent, 'b')

    for bit in binary_exp:
        c = 2 * c
        d = (d * d) % modulus
        if bit == '1':
            c += 1
            d = (d * base) % modulus

    return d


def miller_rabin(n, s):
    """
    An implementation of the Miller-Rabin algorithm for primality testing.
    This method simply generates numbers and calls 'witness()', which performs the actual test.

    This algorithm guarantees a composite result, but not a prime result. The confidence in a prime result goes up
    with a higher value of s.

    :param n: Integer - The number to test for primality, should be greater than 2
    :param s: Integer - The number of random witnesses to test with
    :return: Boolean - True if prime, False if composite
    """
    import random

    # input check to avoid edge cases we can't handle
    # shouldn't ever be needed when used with the main method
    if n < 4:
        return False

    for i in range(0, s):
        a = random.randrange(2, n - 1)
        if witness(a, n):
            return False
    return True


def witness(a, n):
    """
    Part of the Miller-Rabin algorithm for primality testing.

    This implementation comes from Introduction to Algorithms by Cormen, Leiserson, Rivest, Stein, as referenced in
    Professor Kabir's lecture notes.

    :param a: Integer - The witness to test with, 1 < a < n-1
    :param n: Integer - The number to test for primality
    :return: Boolean - True if composite, False if prime
    """

    # input check to avoid edge cases we can't handle
    # shouldn't ever be needed when used with the main method
    if n < 4:
        return False

    # generate t and u such that t >= 1, u is odd, and (n-1 = 2^t * u)
    # this is done by factoring n - 1 by powers of two, using some tricks with binary
    binary = format(n - 1, 'b')  # get a binary representation of n - 1
    t = len(binary) - len(binary.rstrip('0'))  # t is the number of trailing zeros
    u = int(binary.rstrip('0'), 2)  # u is the binary number that results from removing the trailing zeros

    x = [fast_exponent_mod(a, u, n)]

    for i in range(1, t + 1):
        x.append((x[i - 1] * x[i - 1]) % n)
        if x[i] is 1 and x[i - 1] is not 1 and x[i - 1] is not n - 1:
            return True
    if x[t] is not 1:
        return True
    return False


def keygen():
    """
    Generates a random public and private key.
    Each key contains the selected prime, a generator for the prime, and a unique integer.

    The public and private keys are stored in 'pubkey.txt' and 'prikey.txt' respectively.

    :return: The public and private keys, each as a 3-part tuple containing the prime, generator, and key.
    """
    import secrets

    # use '2' as generator 'g'
    g = 2

    # find prime 'p'
    # while True:
    #     while True:
    #         q = secrets.randbits(31)
    #         print(q)
    #         if miller_rabin(q, 5) and q % 12 == 5:
    #             break
    #     p = (2 * q) + 1
    #     if miller_rabin(p, 5):
    #         break
    # print("prime:", p)
    p = 101

    # pick a random secret key 'd'
    d = secrets.randbelow(p)

    # calculate public key 'e2'
    e2 = fast_exponent_mod(g, d, p)

    with open('pubkey.txt', 'w') as file:
        file.write(str(p) + ' ' + str(g) + ' ' + str(e2))

    with open('prikey.txt', 'w') as file:
        file.write(str(p) + ' ' + str(g) + ' ' + str(d))

    return (p, g, e2), (p, g, d)


def encrypt(key_file, text_file):
    pass


def decrypt(key_file, cipher_file):
    pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('key_file')
    parser.add_argument('message_file')
    parser.add_argument('-e', action='store_true')
    parser.add_argument('-d', action='store_true')
    parser.add_argument('-p', action='store_true')

    args = parser.parse_args()

    if args.e:
        encrypt(args.key_file, args.message_file)
    elif args.d:
        decrypt(args.key_file, args.message_file)
    else:
        keys = keygen()
        if args.p:
            print("Public Key: ", keys[0])
            print("Private Key:", keys[1])

    pass
