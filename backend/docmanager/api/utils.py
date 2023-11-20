from cryptography.fernet import Fernet


def generate_key():
    """
    Генерирует ключ для шифрования.

    Returns:
        str: Сгенерированный ключ в виде строки.
    """
    return Fernet.generate_key()


def encrypt_file(file_path, key):
    """
    Шифрует содержимое файла с использованием ключа и сохраняет зашифрованные данные в новом файле.

    Args:
        file_path (str): Путь к файлу, который требуется зашифровать.
        key (str): Ключ для шифрования.

    Returns:
        str: Путь к созданному зашифрованному файлу.
    """
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
