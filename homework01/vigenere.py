def encrypt_vigenere(plaintext, keyword):
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """

    ciphertext = ''
    keyword *= len(plaintext) // len(keyword) + 1
    for i, j in enumerate(plaintext):
        if ord('A') <= ord(j) <= ord('Z'):
            code = chr((ord(j) + ord(keyword[i])) % 26 + ord('A'))
            ciphertext += code
        else:
            code = chr((ord(j) + ord(keyword[i]) + 14) % 26 + ord('a'))
            ciphertext += code
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """

    plaintext = ''
    keyword *= len(ciphertext) // len(keyword) + 1
    for i, j in enumerate(ciphertext):
        if ord('A') <= ord(j) <= ord('Z'):
            code = chr((ord(j) - ord(keyword[i])) % 26 + ord('A'))
            plaintext += code
        else:
            code = chr((ord(j) - ord(keyword[i])) % 26 + ord('a'))
            plaintext += code
    return plaintext
