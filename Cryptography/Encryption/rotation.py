from Cryptography import misc







########################################################################################## STANDARD FUNCTIONS ##########

# Encrypt using user-entered info. Write relevant information and return encrypted text for cryptography_runner
def execute(data, output_location):
    """
    This function calls the appropriate functions in misc.py. Those functions will use the encrypt() function
    located below as the algorithm to actually encrypt the text. Then, the ciphertext will be returned back to
    cryptography_runner.py

    :param data: (string) the data to be encrypted
    :param output_location: (string) the location to print out the information
    :return: (string) the encrypted data
    """

    # Encrypt the plaintext. Print out the ciphertext and relevant information
    misc.execute_encryption_or_decryption(data, output_location, "Encryption", "rotation", "encrypt")





# This function contains the actual algorithm to encrypt in a rotation cipher using a key
def encrypt(plaintext, key, alphabet_size):
    """
    This function encrypts the plaintext using the set of unicode characters from 0 to alphabet_size - 1.

    :param plaintext: (string )the text to be encrypted
    :param key: (string) the key with which the encryption is done
    :param alphabet_size: (int) The number of characters in the character set
    :return: (string) the encrypted text
    """

    encrypted = "" # the string to build up the encrypted text
    key_index = 0 # the index in the key we are using for the vigenere encrypt


    for x in plaintext:



        uni_val_plain = ord(x)                       #  figure out the unicode value for the current character
        uni_val_key = ord(key[key_index])            #  figure out the unicode value for the right character in the key



        #  figure out the character by combining the two ascii's, the add it to the encrypted string
        encrypted_char = chr((uni_val_plain + uni_val_key) % (alphabet_size))
        encrypted = encrypted + encrypted_char





    return encrypted







