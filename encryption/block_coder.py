import cv2 as cv
import numpy as np
import math

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

def xor(one, two):
    result = []
    for i in range(len(one)):
        result.append(one[i] ^ two[i])
    return result

def block_coder(one, two):
    # In reality, this would be a more complex operation, such as a sequence of
    # [s-boxes](https://de.wikipedia.org/wiki/S-Box).
    return xor(one, two)

def block_encrypt(plain_bytes, key_bytes, previous_block):
    # Chaining Block Cipher: Encrypt a single block but first 
    # xor the previous encrypted block with the plain text.
    return block_coder(xor(plain_bytes, previous_block), key_bytes)

def block_decrypt(cipher_bytes, key_bytes, previous_block):
    # Chaining Block Cipher: Encrypt a single block but first 
    # xor the previous encrypted block with the plain text.
    return xor(block_coder(cipher_bytes, key_bytes), previous_block)

def chain_encrypt(plain_bytes, key_bytes, initialization_vector='12345678'):
    block_size = len(initialization_vector)
    iv = text_to_bytes(initialization_vector)

    # ensure our key material is divisible by block_size
    key_bytes = key_bytes * block_size

    first_block = text_to_bytes('a'*block_size)
    cipher_bytes = block_encrypt(first_block, key_bytes[0:block_size], iv)
    previous_block = cipher_bytes

    for i in range(0, len(plain_bytes), block_size):
        plain_block = plain_bytes[i:i+block_size]
        key_index = i % len(key_bytes)
        key_block = key_bytes[key_index:key_index+block_size]
        cipher_block = block_encrypt(plain_block, key_block, previous_block)
        cipher_bytes += cipher_block
        previous_block = cipher_block
    
    return cipher_bytes

def chain_decrypt(cipher_bytes, key_bytes, block_size = 8):
    # ensure our key material is divisible by block_size
    key_bytes = key_bytes * block_size

    previous_block = cipher_bytes[0:block_size]
    plain_bytes = []

    # The decrypted first block is ignored...
    for i in range(block_size, len(cipher_bytes), block_size):
        cipher_block = cipher_bytes[i:i+block_size]
        key_index = i % len(key_bytes)
        key_block = key_bytes[key_index:key_index+block_size]
        plain_block = block_decrypt(cipher_block, key_block, previous_block)
        plain_bytes += plain_block
        previous_block = cipher_block
    return plain_bytes

key_bytes = text_to_bytes("ROMANSHO")
print(bytes_to_text(chain_decrypt(chain_encrypt(text_to_bytes("Eine richtig geheime Botschaft!"), key_bytes), key_bytes)))