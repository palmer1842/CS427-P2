CS427 Project 2 -- 4/18/20
Public Key Cryptosystem
Jake Palmer --- jake.palmer@wsu.edu

Project Overview:
  This project provides a complete public key cryptography system. Users can generate a key pair and use it to
  encrypt and decrypt messages.

  To use the system, first generate a keypair and share the public key with the party you would like to securely
  communicate with. Keys include the following parameters:
    p - a 33 bit prime, included with both keys
    g - a primitive root of p, included with both keys
    d - the 'private key', a random integer less than p
    e2 - the 'public key', a unique integer calculated from the private key
  The prime 'p' is calculated in such a way that it's generator is always 2. The Miller-Rabin algorithm is used to
  check prime candidates.

  Using a public key, the user can encrypt an ASCII text file. The file is encrypted in 32 bit 'blocks', with each block
  becoming a pair of integers. The program will output a cipher text file called 'ctext.txt', which will contain the
  integer pairs.

  Using the corresponding private key, a cipher text can be decrypted. The decrypted message will be
  output into a file called 'dtext.txt'.

Included Files:
  public-key-cryptosystem.py --- The program, containing key gen, encryption, decryption, and helper methods
  README.txt -- documentation

Running:
  The program can be run with python 3.

    python3 public-key-cryptosystem.py [-h] ("keygen" | keyfile textfile) [-e | -d]

  Running with the single argument 'keygen' will generate a public and private key pair, and store them in 'pubkey.txt'
  and 'prikey.txt'.

  Running with -e or -d will encrypt or decrypt respectively, using the key from 'keyfile' and plaintext or cipher text
  from 'textfile'.

  When encrypting, provide the public key stored in pubkey.txt. When decrypting, provide the private key stored in
  prikey.txt. The text file will be either be a plaintext message to encrypt, or a cipher text file to decrypt.
