from cryptography.fernet import Fernet
import secrets

def encrypt_text(value):
	key_value=[]
	encrypt_value=[]
	for i in range(6):
		key_value.append(secrets.randbelow(10))

	for i in range(0,len(value)):
		encrypt_value.append(chr(ord(value[i])+key_value[i%6]))
	print(encrypt_value)
	decrypt_text(encrypt_value,key_value)
	pass

def decrypt_text(value,key):
	encrypt_value=[]
	for i in range(0,len(value)):
		encrypt_value.append(chr(ord(value[i])-key[i%6]))
	print(encrypt_value)
	pass

def encrypt_file(value):
	pass

def decrypt_file(value,key):
	pass

encrypt_text('hello')
