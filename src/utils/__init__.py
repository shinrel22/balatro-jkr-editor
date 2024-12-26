import zlib
from cryptography.fernet import Fernet


def decompress_data(data: bytes,
               encryption_key: str = None,
               wbits: int = None
               ) -> bytes:

    if encryption_key:
        cipher_suite = Fernet(encryption_key)
        data = cipher_suite.decrypt(data)

    options = dict()
    if wbits:
        options['wbits'] = wbits

    return zlib.decompress(data, **options)

def compress_data(data: bytes, encryption_key: str = None, level: int = None, wbits: int = None) -> bytes:
    options = dict()
    if level is not None:
        options['level'] = level
    if wbits is not None:
        options['wbits'] = wbits

    compressor = zlib.compressobj(**options)
    compressed_data = compressor.compress(data) + compressor.flush()

    if encryption_key:
        cipher_suite = Fernet(encryption_key)
        compressed_data = cipher_suite.encrypt(compressed_data)

    return compressed_data
