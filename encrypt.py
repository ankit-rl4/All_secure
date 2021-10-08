from cryptography.fernet import Fernet
import secrets

def encrypt_text(value):
	key_value=[]
	encrypt_value=[]
	for i in range(6):
		key_value.append(secrets.randbelow(10))

	for i in range(0,len(value)):
		encrypt_value.append(chr(ord(value[i])+key_value[i%6]))
	key_value=numlisttostr(key_value)
	return listToString(encrypt_value), key_value

def decrypt_text(value,key):
	decrypt_value=[]
	for i in range(0,len(value)):
		decrypt_value.append(chr(ord(value[i])-key[i%6]))
	return listToString(decrypt_value)

def listToString(s):
	str1 = ""
	for ele in s:
		str1 += ele
	return str1

def numtolist(s):
	listn=[]
	for n in s:
		listn.append(int(n))
	return listn

def numlisttostr(z):
	str1 = ""
	for ele in z:
		str1 += str(ele)
	return str1