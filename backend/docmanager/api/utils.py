from cryptography.fernet import Fernet
import json
import os


def generate_key():
    return Fernet.generate_key()


def encrypt_file(file_path, key):
    cipher_suite = Fernet(key)

    with open(file_path, 'rb') as file:
        file_data = file.read()

    encrypted_data = cipher_suite.encrypt(file_data)

    encrypted_file_path = file_path + '.enc'
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

    return encrypted_file_path


key = generate_key()
with open('.env', 'w') as env_file:
    env_file.write(f'ENCRYPTION_KEY={key.decode()}')


# Шифрование файла credentials.json
encrypted_credentials_path = encrypt_file('credentials.json', key)
print(f'Encrypted file saved at: {encrypted_credentials_path}')
print(f'Decryption key: {key.decode()}')
encrypted_token_path = encrypt_file('token.json', key)
print(f'Encrypted file saved at: {encrypted_token_path}')
print(f'Decryption key: {key.decode()}')
