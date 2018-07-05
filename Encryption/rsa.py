import miscellaneous  # To handle user input and miscellaneous
import time # To measure the amount of time for finding a public key
from Decryption import rsa # To save variables there






# Bit-size of the key (should be divisible by 12 for character schemes)
key_size = 2048



# Encrypt using user-entered info. Write relevant information and return encrypted text for cryptography_runner
def execute(data, output_location):
    """
    This function calls the appropriate functions in miscellaneous.py. Those functions will use the encrypt() function
    located below as the algorithm to actually encrypt the text. Then, the ciphertext will be returned back to
    cryptography_runner.py

    :param data: (string) the data to be encrypted
    :param output_location: (string) the location to print out the information
    :return: (string) the encrypted data
    """

    # Obtain the encrypted text. Also write statistics and relevant info a file
    encrypted = miscellaneous.asymmetric_encrypt_and_generate_keys(data, output_location, "Encryption", "rsa",
                                                                   "encrypt")

    # Return encrypted text to be written in cryptography_runner
    return encrypted







# The actual algorithm to encrypt using rsa encryption
def encrypt(plaintext, given_key, char_set_size):
    """
    This encrypts using an rsa encryption. Random primes for the key are generated.

    :param plaintext: (string) the data to be encrypted
    :param given_key: (string) the public key used for encryption (not a requirement)
    :param key: (string) NOT USED
    :param char_set_size: (int) the size of the character set
    :return: (string) the encrypted text
    :return: (string) the generated public key for this in string form
    :return: (string) the generated private key for this in string form
    """

    global key_size; rsa.key_bits = key_size # the bit size of the key (needs to be divisible by 8)
    ciphertext = ""  # the string to build up the encrypted text
    prime_num_one = 0  # one of the randoly generated prime numbers
    prime_num_two = 0  # the other randomly generated prime numbers
    public_key = ""
    private_key = ""
    e = 0 # the public encryption key (the actual number)
    d = 0 # the private encryption key (the actual number)
    n = 0 # the modulus for the encryption  (the number)

    # Figure out which char encoding scheme to use(reverse dictionary lookup)
    char_encoding_scheme = [key for key,
                            value in miscellaneous.char_set_to_char_set_size.items() if value == char_set_size][0]


    # If the public key (given_key) not given, then generate public and private keys (while also generating the two
    # primes necessary for the keys)
    if given_key == "":

        # Generate two prime numbers that when multiplied together results in n with bit_length() of key_size. Two
        # prime numbers of size prime_bit_length may not necessarily result in a key_size of the 2 * prime_bit_length
        start_time = time.time()
        prime_one, prime_two = miscellaneous.get_prime_pair(key_size); rsa.time_to_generate_keys = time.time() - \
                                                                                                  start_time


        # Calculate the public key and the private key
        e, d, n, public_key, private_key = _calculate_public_and_private_key(prime_one, prime_two, char_encoding_scheme)

    # Else, parse public_key to figure out e and n.
    else:
        e, n = miscellaneous.read_rsa_key(given_key)




    # Convert the plaintext into a long string of hex digits (through utf-8 interpretation). Divide the hex digits
    # into blocks of key_size // 8 bytes (the maximum that rsa can encrypt). Turn each of those hex blocks into
    # integers, and encrypt them each. Lastly, transform each of those ints into characters thorugh a character
    # encoding scheme, and concatenate the results together to get the ciphertext
    plaintext = plaintext.encode("utf-8") # After utf-8 encoding, is a bytearray
    plaintext = plaintext.hex() # Change into hex for easier conversion into ints

    # Divide the hexadecimal digits of plaintext into key_size//8 blocks. Store blocks in a list. Store num of blocks
    plaintext_blocks = []
    while plaintext != "":
        plaintext_blocks.append( plaintext[0: key_size // 8] )
        plaintext = plaintext[key_size // 8:]
    rsa.num_blocks = len(plaintext_blocks)

    # Turn each plaintext block from a string of hex digits into an integer
    plaintext_blocks = [int(block, 16) for block in plaintext_blocks]

    # For each block, run encryption with public key e. Then, turn the ciphertext number into characters with the
    # chosen character scheme
    ciphertext_blocks = [ pow(block, e, n) for block in plaintext_blocks ]
    ciphertext_blocks = [ miscellaneous.int_to_chars_encoding_scheme_pad(block, char_encoding_scheme, key_size)
                                        for block in ciphertext_blocks] ;rsa.block_size = (len(ciphertext_blocks[0]))


    # Concatenate all of the blocks to form the ciphertext
    for block in ciphertext_blocks:
        ciphertext += block


    # return ciphertext
    return ciphertext, public_key, private_key








def _calculate_public_and_private_key(prime_one, prime_two, char_encoding_scheme):
    """
    Given two primes, calculate the private and public key

    :param prime_one: (int) a prime
    :param prime_two: (int) another prime
    :param char_encoding_scheme: (string) tells us which character set to use to render the public/private
    keys as text
    :return: (int) encryption number e
    :return: (int) decryption number d
    :return: (int) modulus number n
    :return: (string) public key in format "e = ..., n = ..."
    :return:(string) private key in format "d = ..., n = ..."
    """
    two_bytes = 16
    modulus = prime_one * prime_two  # Calculate hte modulus by multiplying the two primes together
    modulus_totient = (prime_one - 1) * (
            prime_two - 1)  # Calculate totient speedily(using properties of primes)

    e = 65537  # Commonly used as e for low hamming weight, among other reasons

    # Calculate d (modular multiplicative inverse of (e mod n). Compute with extended euclidean algorithm
    def inverse(x, modulus):

        # Extended euclidean algorithm
        a, b, u = 0, modulus, 1
        while x > 0:
            # Figure out the integer quotient
            quotient = b // x

            # Update for next iteration
            x, a, b, u = b % x, u, x, a - (quotient * u)

        # Calculate the modular multiplicative inverse by a % m
        if b == 1:
            return a % modulus
    d = inverse(e, modulus_totient)

    # Save integer values of e, d, and modulus for return
    e_num = e
    d_num = d
    modulus_num = modulus

    # Convert d  and e, and modulus from numbers to encoded character version. Also do e and d's lengths
    e = miscellaneous.int_to_chars_encoding_scheme(e, char_encoding_scheme)
    e_len = len(e)
    d = miscellaneous.int_to_chars_encoding_scheme(d, char_encoding_scheme)
    d_len = len(d)
    modulus = miscellaneous.int_to_chars_encoding_scheme(modulus, char_encoding_scheme)

    # Build up the public and private keys strings. Then encode them using whichever scheme
    public_key = "RSA: " + str(e_len) + " " + e + modulus
    private_key = "RSA: " + str(d_len) + " " + d + modulus
    public_key = miscellaneous.chars_to_chars_encoding_scheme(public_key, char_encoding_scheme)
    private_key = miscellaneous.chars_to_chars_encoding_scheme(private_key, char_encoding_scheme)

    # Return the public and private keys
    return e_num, d_num, modulus_num, public_key, private_key









