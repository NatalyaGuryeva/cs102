def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ''
    for symb in plaintext:
        code = ord(symb)
        if ord('a') <= code <= ord('z') or ord('A') <= code <= ord('Z'):
            code = code + 3
            ciphertext += chr(code)
        if code > ord ('z') or code < ord('a') and code > ord('Z'):
            code -= 26
            ciphertext += chr(code)
        else:
            ciphertext += symb

    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """

    plaintext = ''
    for symb in ciphertext:
        code = ord(symb)
        if ord('a') <= code <= ord('z') or ord('A') <= code <= ord('Z'):
            code = code - 3
            plaintext += chr(code)
        if code > ord('z') or code < ord('a') and code > ord('Z'):
            code += 26
            plaintext += chr(code)
        else:
            plaintext += symb
    return plaintext
