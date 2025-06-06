import cv2 as cv
import numpy as np
import math
import random

def text_to_bytes(text):
    """Converts a string into a list of ASCII codes."""
    numbers = []
    for letter in text:
        number = ord(letter)
        numbers.append(number)
    return numbers

def bytes_to_text(numbers):
    """Converts a number list into text using ASCII decoding."""
    text = ""
    for number in numbers:
        letter = chr(number)
        text += letter
    return text

def binary_to_bytes(binstring):
    binstring *= 8  # ensure we are byte-aligned
    result = []
    for eight in range(0, len(binstring), 8):
        result.append(int(binstring[eight:eight+8], 2))
    return result

def xor(one, two):
    result = []
    for i in range(len(one)):
        result.append(one[i] ^ two[i])
    return result

def block_encrypt(one, two):
    # In reality, this would be a more complex operation, such as a sequence of
    # [s-boxes](https://de.wikipedia.org/wiki/S-Box).
    return xor(one, two)

def block_decrypt(one, two):
    # In reality, this would be the inverse of block_encrypt.
    return xor(two, one)

def encrypt(plain_bytes, key_bytes, chaining=True, block_size=8):
    # random initialization vector
    iv = random.randbytes(block_size)

    # ensure our key material is divisible by block_size
    key_bytes = key_bytes * block_size

    first_block = text_to_bytes('a'*block_size)
    cipher_bytes = block_encrypt(xor(first_block, iv), key_bytes[0:block_size])
    previous_block = cipher_bytes

    for i in range(0, len(plain_bytes), block_size):
        plain_block = plain_bytes[i:i+block_size]
        key_index = (i+block_size) % len(key_bytes)
        key_block = key_bytes[key_index:key_index+block_size]
        if chaining:
            plain_block = xor(plain_block, previous_block)
        cipher_block = block_encrypt(plain_block, key_block)
        cipher_bytes += cipher_block
        previous_block = cipher_block
    
    return cipher_bytes

def decrypt(cipher_bytes, key_bytes, chaining=True, block_size = 8):
    # ensure our key material is divisible by block_size
    key_bytes = key_bytes * block_size

    # the first block is thrown away
    previous_block = cipher_bytes[0:block_size]
    plain_bytes = []

    # The decrypted first block is ignored...
    for i in range(block_size, len(cipher_bytes), block_size):
        cipher_block = cipher_bytes[i:i+block_size]
        key_index = i % len(key_bytes)
        key_block = key_bytes[key_index:key_index+block_size]
        plain_block = block_decrypt(cipher_block, key_block)
        if chaining:
            plain_block = xor(plain_block, previous_block)
        plain_bytes += plain_block
        previous_block = cipher_block
    return plain_bytes


def bytes_to_image(img_bytes, shape):
    as_np = np.asarray(img_bytes, order='C', dtype="uint8")
    as_np = as_np.reshape(shape)
    return as_np

# Play with different keys:
#key = "11110000011001101100010000110101110010111001100100010110000111110001100101000101101110111111000000000011000000111110010111101010111110001110101010101000001111001010110110100111000000000011111111010001111100110111101001111010000001011101010000101111110101001100010101001011011101110101011001110100100001101110110011000110100100111100010011001100100111000000000011011110000100010010001110101100111101010100111100010001010100101100111101101011100110110000000000101000000010100111110010000011101000111001100000101011110000000100110011000001000101001000011101000100100100100010100111110011101011010101010110001011010001001010000111000100100010111001111100011100001000011001100011100110101101111001000110001001111010111111100001111111111111011101100101111100000101000101100101011111111110001010111000101010110011011010111111101111110100000100100101001000100101100111100010101011111111001001101000011001101111000111111110101100001100110110000101100000000010111110001011011010010010000111010010011001101010010100000011101111110100101001111110011010000101001111001111000000010101111001000101100110010111101111001000010110111101000110110101000101110001001011100111110010111001011111111010000010011000011101100110111001001000110001110110011011000011001010001111000101100100001010110011000001011100001011010011010001110101010001111000000111111101110011000010010000111010111000111000110"
key = "1111000001100110110001000011010111001011100110010001011000011111000110010100010110"
key_bytes = binary_to_bytes(key)
#key_bytes = text_to_bytes("rõménshÖRÑ")
key_bytes = text_to_bytes("ROMANSHORN")

# Change between ECB and CBC modes:
chaining = False  # False: ECB, True: CBC

img = cv.imread('encryption/penguin.png')
img_bytes = img.tobytes()

img_encrypted = encrypt(img_bytes, key_bytes, chaining=chaining)

# We drop the first block as it's only used as initialization vector.
cv.imshow("image", bytes_to_image(img_encrypted[8:], img.shape))
cv.waitKey()

# Test if decryption works
# img_decrypted = decrypt(img_encrypted, key_bytes, chaining=chaining)
# cv.imshow("image", bytes_to_image(img_decrypted, img.shape))
# cv.waitKey()