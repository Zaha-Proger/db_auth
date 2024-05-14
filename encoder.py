from cryptography.fernet import Fernet
import os

class Encoder():
    def __init__(self, path):
        key_file = open('crypto.key', 'wb+')
        if os.path.getsize('crypto.key') != 0:
            key = key_file.read()
        else:
            key = Fernet.generate_key()
            key_file.write(key)
        key_file.close()
        self.fernet = Fernet(key)
        self.f_name = path

    def encrypt_file(self):
        # Зашифруем файл и записываем его
        with open(self.f_name, 'rb') as file:
                # прочитать все данные файла
                file_data = file.read()
                # записать зашифрованный файл
        encrypted_data = self.fernet.encrypt(file_data)
        with open(self.f_name, 'wb') as file:
            file.write(encrypted_data)

    def decrypt_file(self):
        # Расшифруем файл и записываем его
        with open(self.f_name, 'rb') as file:
            # читать зашифрованные данные
            encrypted_data = file.read()
        # расшифровать данные
        decrypted_data = self.fernet.decrypt(encrypted_data)
        # записать оригинальный файл
        with open(self.f_name, 'wb') as file:
            file.write(decrypted_data)