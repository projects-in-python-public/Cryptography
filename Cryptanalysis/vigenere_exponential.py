import miscellaneous
import time
from decimal import * #  use exact decimals to calculate nth roots
getcontext().prec = 3 #  not much precision is necessary



char_sets = ["unicode", "ascii", "extended_ascii"] #  unicode has max val of 1114111,
                                 #  ascii has max val of 127




def decrypt(data, output_location):
    """
    This function decrypts data using a key.

    :param data: the data to be decrypted
    :return: the decrypted data
    """

    #  FIGURE OUT THE CHARACTER SET THAT THE USER WANTS TO USE
    vig_type = miscellaneous.take_char_set(char_sets)

    #  TAKE A KEY
    key = input("Enter the key exactly: ")

    # IF THE USER DIDN"T ENTER ANYTHING, SEND AN ERROR MESSAGE AND ASK AGAIN
    while key == "":
        key = input("No key entered! Enter a key: ")


    # START THE TIMER
    start_time = time.time()

    # EXECUTE THE SPECIFIC ENCRYPTION METHOD
    decrypted = eval("vig_" + vig_type + "(data, key)")

    #  END THE TIMER
    elapsed_time = time.time() - start_time

    #  WRITE TO A NEW FILE CONTAINING THE VIGENERE TYPE, KEY, AND SECONDARY KEY, AND TIME ELAPSED, AND TIME PER
    #     CHARACTER
    new_file = open(output_location + "_(Relevant information)", "w", encoding="utf-8")
    new_file.writelines(["The character set is : " + vig_type,
                         "\nThe key is: " + key,
                         "\n Encoded/decoded in: " + str(elapsed_time) + " seconds.",
                         "\n That is " + str((elapsed_time/len(decrypted) * 1000000)) + " microseconds per character."])

    return decrypted

#  END OF DEF DECRYPT()





def vig_unicode(cipher_text, key):
    """
    This function decrypts the plain text using the unicode character sets, which has a max value of 1114111. Should
    any of the singular values exceed 1114111, it starts from 0 again. For example, 1114112 would become 0.

    :param cipher_text: the text to be decrypted
    :param key: the key with which the decryption is done
    :return: the decrypted text
    """

    decrypted = ""
    key_count = 0
    MAX_CHAR_SET_VAL = 1114112


    SURROGATE_LOWER_BOUND = 55296
    SURROGATE_UPPER_BOUND = 57343
    SURROGATE_BOUND_LENGTH = 57343 - 55296 + 1  # equal to 2048


    ADJUSTED_MAX_CHAR_SET_VAL = MAX_CHAR_SET_VAL - SURROGATE_BOUND_LENGTH
    counter = 0

    for x in cipher_text:
        #  figure out the unicode value for each of the characters
        uni_val_cipher = ord(x)


        #  adjust uni_val_cipher to fit into the adjusted max character set (without the surrogates)
        if uni_val_cipher >= SURROGATE_UPPER_BOUND + 1:
            uni_val_cipher = uni_val_cipher - SURROGATE_BOUND_LENGTH


        #  figure out the unicode value for the right character in the key, then update for next iteration
        key_char = key[key_count]
        uni_val_key = ord(key_char)
        key_count = (key_count + 1) % len(key)



        #  cycle through all possible uni_val_plain, and take that to the power of uni_val_key
        for y in range(1, ADJUSTED_MAX_CHAR_SET_VAL - 1):
            power_result = y ** uni_val_key

            #  check if this power result modded by ADJUSTED_MAX_CHAR_SET_VAL equal to uni_val_cipher. If yes, break
            if power_result % ADJUSTED_MAX_CHAR_SET_VAL == uni_val_cipher:
                uni_val_plain = y
                break



        decrypted_char = chr(uni_val_plain)
        decrypted = decrypted + decrypted_char



        #  give the user an update every thousand characters
        if counter % 1000 == 0:
            print("Characters decrypted: " + str(counter))
        counter = counter + 1

    #  END OF LOOP TO DECRYPT ONE CHARACTER




    return decrypted
#  END OF DEF VIG_UNICODE