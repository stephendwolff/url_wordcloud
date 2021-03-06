# -*- coding: utf-8 -*-
import hashlib

# defining salt in code, as it is just being used to create a primary key, which is repeatable
# this doesn't need to be secret, just hard to identify
# however, the salt should be external to the code repository, probably stored alongside the private key
# These could be stored GPG encrypted, with a limited set of private keys for decryption (ie during deployment)

# also, i'm not sure what the rationale is to use a salt on an index,
# the use case is very different to password confirmation.
# if it is just to show that candidate can salt a hash on the way into the db, then a random salt can be used
import os

from nacl import encoding
from nacl.public import SealedBox, PrivateKey, PublicKey

SALT = "abcdef1234567890"


def generate_keys():
    # Generate applications public and private key
    # In practice, these would be set externally and stored outside the repository
    sk = PrivateKey.generate()
    pk = sk.public_key

    # write to filesfor access if they don't exist
    sk_path = os.path.join(os.path.dirname(__file__), "..", "private_key")
    if not os.path.exists(sk_path):
        # write as binary
        with open(sk_path, 'wb') as f:
            sk_bytes = bytes(sk)
            f.write(sk_bytes)

    pk_path = os.path.join(os.path.dirname(__file__), "..", "public_key")
    if not os.path.exists(pk_path):
        with open(pk_path, 'wb') as f:
            pk_bytes = bytes(pk)
            f.write(pk_bytes)


def salted_hash(text):
    """

    :param text: text string to be salted and hashed
    :return: string of hash as hexadecimal digits
    """
    return hashlib.sha512((text + SALT).encode('utf-8')).hexdigest()


def asymmetrically_encrypt(text, pk):
    """

    :param text: bytestring to be encrypted
    :param pk: binary public key (from file)
    :return: encrypted word as hexadecimal string
    """
    public_key = PublicKey(pk)
    sealed_box = SealedBox(public_key)
    encrypted_bytestring = sealed_box.encrypt(text.encode('utf-8'), encoder=encoding.HexEncoder)
    return str(encrypted_bytestring, "utf-8")


def asymmetrically_decrypt(text, sk):
    """

    :param text: hexadecimal string to be decrypted
    :param sk: private key [binary] from file
    :return:
    """

    private_key = PrivateKey(sk)
    sealed_box = SealedBox(private_key)
    return sealed_box.decrypt(text, encoder=encoding.HexEncoder)
