import miscellaneous




# Cipher info:
alphabet = miscellaneous.char_sets
key_type = "symmetric"






# Decrypt using user-entered info. Write relevant information and return decrypted text for cryptography_runner
def execute(data, output_location):
    """
    This function decrypts data using a user-provided key.

    :param data: (string) the data to be decrypted
    :param output_location: (string) the location to write out relevant info and statistics
    :return: (string) the decrypted data
    """

    # Obtain the decrypted text. Also write statistics and relevant info to a file
    decrypted = miscellaneous.symmetric_ed_with_single_char_key(data, output_location,
                                                                      "Decryption", "rotation", "decrypt")


    # Return encrypted text to be written in cryptography_runner
    return decrypted




# Decrypt in testing mode. So add more statistics about performance. Check for correctness
def testing_execute(ciphertext, output_location, plaintext, key, char_set_size, encryption_time):
    """
    Conducts a rotation decryption in testing mode

    :param ciphertext: (string) the ciphertext to decrypt
    :param output_location: (string) the file to store statistics about decryption
    :param plaintext: (string) the plaintext to check for correctness
    :param key: (string) the key to decrypt with
    :param char_set_size: (integer) the size of the character set used
    :param encryption_time: (double) the time that encryption took
    :return: None
    """

    # Encryption code
    encryption_code = miscellaneous.general_encryption_code

    # Decryption code
    decryption_code = miscellaneous.general_decryption_code

    miscellaneous.testing_general_decrypt_with_key(ciphertext, output_location, plaintext, key, key, char_set_size,
                                                   encryption_time, "Decryption", "rotation",
                                                   "Rotation", "decrypt", encryption_code,
                                                   decryption_code)





# This function contains the actual algorithm to decrypt a rotation cipher with a key
def decrypt(ciphertext, key, char_set_size):
    """
    This function decrypts the ciphertext using the set of unicode characters from 0 to end_char.

    :param ciphertext: (string )the text to be encrypted
    :param key: (string) the key with which the encryption is done
    :param char_set_size: (int) The number of characters in the character set
    :return: (string) the encrypted text
    """

    encrypted = "" # the string to build up the encrypted text
    key_index = 0 # the index in the key we are using for the vigenere encrypt


    for x in ciphertext:
        #  figure out the unicode value for the current character
        uni_val_cipher = ord(x)

        #  figure out the unicode value for the right character in the key. THen, update key_index for next iteratio
        uni_val_key = ord(key[key_index])
        key_index = (key_index + 1) % len(key)


        #  figure out the character by subtracting the two ascii's, the add it to the encrypted string
        encrypted_char = chr((uni_val_cipher - uni_val_key) % (char_set_size))
        encrypted = encrypted + encrypted_char



    return encrypted


