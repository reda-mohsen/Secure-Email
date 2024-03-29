import os
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES


def encrypt_file(key, in_filename, out_filename=None, chunksize=16):
    """
    Encrypts a file using AES (CBC mode) with the given key.

    key: The encryption key - a string that must be either 16, 24, or 32 bytes long. Longer keys are more secure.
    in_filename: Name of the input file.
    out_filename: If None, '<in_filename>.enc' will be used.
    chunksize: Sets the size of the chunk which the function uses to read and encrypt the file.
    Larger chunk sizes can be faster for some files and machines. chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    encryptor = AES.new(key, AES.MODE_ECB)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)
                outfile.write(encryptor.encrypt(chunk))


def decrypt_file(key, in_filename, out_filename=None, chunksize=16):
    """
    Decrypts a file using AES (CBC mode) with the given key.

    Parameters are similar to encrypt_file, with one difference: out_filename, if not supplied,
    will be in_filename without its last extension
    (i.e. if in_filename is 'aaa.zip.enc' then out_filename will be 'aaa.zip').
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        decryptor = AES.new(key, AES.MODE_ECB)
        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))


# kk = b'\xcek\xacd~@\x10\xee3:JW\x99\xda\xe2\x02'
# encrypt_file(kk,'in.txt','out.txt')
# decrypt_file(kk,'out.txt','dec.txt')

# Generate two random keys to be used as a secret keys in sender and receiver sides.
# for i in range(2):
#     Random_Key = get_random_bytes(16)
#     print(Random_Key)
