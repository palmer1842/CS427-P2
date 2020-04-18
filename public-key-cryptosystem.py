import secrets


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

    # generate t and u such that t >= 1, u is odd, and (n-1 = 2^t * u)
    # this is done by factoring n - 1 by powers of two, using some tricks with binary
    u = n - 1
    t = 0
    while (u & 0b1) != 1:
        u //= 2
        t += 1

    for i in range(0, s):
        a = random.randrange(2, n - 1)
        if witness(a, n, t, u):
            return False
    return True


def witness(a, n, t, u):
    """
    Part of the Miller-Rabin algorithm for primality testing.

    This implementation comes the Wikipedia Article "Miller–Rabin primality test"

    :param a: Integer - The witness to test with, 1 < a < n-1
    :param n: Integer - The number to test for primality
    :param u: Integer - A pre-calculated value used in the algorithm
    :param t: Integer - A pre-calculated value used in the algorithm
    :return: Boolean - True if composite, False if prime
    """

    # Wikipedia's Algorithm:
    x = fast_exponent_mod(a, u, n)
    if x == 1 or x == (n - 1):
        return False
    for i in range(0, t - 1):
        x = fast_exponent_mod(x, 2, n)
        if x == n - 1:
            return False
    return True


def keygen():
    """
    Generates a random public and private key.
    Each key contains the selected prime, a generator for the prime, and a unique integer.

    The public and private keys are stored in 'pubkey.txt' and 'prikey.txt' respectively.

    :return: The public and private keys, each as a 3-part tuple containing the prime, generator, and key.
    """

    # use '2' as generator 'g'
    g = 2

    # find prime 'p'
    while True:
        while True:
            q = secrets.randbits(32)
            q = q | 2147483649  # ensure that 32nd bit is high and the number is odd
            if miller_rabin(q, 100) and q % 12 == 5:
                break
        p = (2 * q) + 1
        if miller_rabin(p, 100):
            break

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
    """
    Encrypts an ASCII text file using a public key generated from keygen()
    The resulting cipher text is written to a file called 'ctext.txt'

    :param key_file: A text file containing the public key in the form 'p g e2'
    :param text_file: An ASCII text file containing a plaintext message to encrypt
    :return: Nothing
    """
    # read in public key from key_file
    with open(key_file, 'r') as file:
        key = file.read().split(' ')
        p = int(key[0])
        g = int(key[1])
        e2 = int(key[2])

    with open(text_file, 'r') as message_file:
        with open('ctext.txt', 'w') as cipher_file:
            while True:
                m, eof = getblock(message_file)
                k = secrets.randbelow(p)
                c1 = fast_exponent_mod(g, k, p)
                c2 = (fast_exponent_mod(e2, k, p) * (m % p)) % p
                print("C1:", c1)
                print("C2:", c2)
                cipher_file.write(str(c1) + ' ' + str(c2) + ' ')

                if eof:
                    break


def getblock(file):
    """
    A helper method for encrypt()
    Reads a 32 bit block from a given ASCII text file

    :param file: The file to read
    :return: A 32 bit integer block, and EOF status
    """
    eof = False
    block = 0

    for i in range(4):
        char = file.read(1)
        if char == '':
            char = '0'
            eof = True
        block = (block << 8) ^ ord(char)
    return block, eof


def decrypt(key_file, cipher_file):
    """
    Decrypts a cipher text file created with encrypt(), using a private key generated with keygen()
    The file is assumed to be an ASCII text file containing a series of integers separated by spaces

    The resulting plaintext is written to a file called 'dtext.txt'

    :param key_file: A text file containing the public key in the form 'p g d'
    :param cipher_file: An ASCII text file containing the cipher text to decrypt
    :return: Nothing
    """
    # read in private key from key_file
    with open(key_file, 'r') as file:
        key = file.read().split(' ')
        p = int(key[0])
        g = int(key[1])  # the generator isn't actually needed for decryption
        d = int(key[2])

    with open(cipher_file, 'r') as cipher_file:
        with open('dtext.txt', 'w') as decryption_file:
            while True:
                c1, eof = readint(cipher_file)
                c2, eof = readint(cipher_file)
                if eof:
                    break
                m = (fast_exponent_mod(c1, p - 1 - d, p) * (c2 % p)) % p
                # convert integer message block to ASCII characters
                m1 = (m >> 24) & 0xFF
                m2 = (m >> 16) & 0xFF
                m3 = (m >> 8) & 0xFF
                m4 = m & 0xFF
                print("Message block: " + str(m) + ' -> ' + chr(m1) + chr(m2) + chr(m3) + chr(m4))
                decryption_file.write(chr(m1) + chr(m2) + chr(m3) + chr(m4))


def readint(file):
    """
    A helper method for decrypt()
    Reads and converts a single integer from the input file

    :param file: The file to read
    :return: A single integer and EOF status
    """
    eof = False
    num = ''
    while True:
        # build the number one character at a time
        nextnum = file.read(1)
        if nextnum == ' ':
            break
        if nextnum == '':
            num = 0
            eof = True
            break
        num += nextnum
    return int(num), eof


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(usage='public-key-cryptosystem.py [-h] ("keygen" | keyfile textfile) [-e | -d]')
    parser.add_argument('key_file')
    parser.add_argument('text_file', nargs='?')
    parser.add_argument('-e', action='store_true')
    parser.add_argument('-d', action='store_true')
    parser.add_argument('-p', action='store_true')

    args = parser.parse_args()

    if args.key_file == 'keygen':
        keys = keygen()
        print("Public Key: ", keys[0])
        print("Private Key:", keys[1])
    elif args.e:
        if not args.text_file:
            parser.print_usage()
            print("Error: No text file given to encrypt")
            exit(1)
        encrypt(args.key_file, args.text_file)
    elif args.d:
        if not args.text_file:
            parser.print_usage()
            print("Error: No text file given to decrypt")
            exit(1)
        decrypt(args.key_file, args.text_file)
    else:
        parser.print_usage()
