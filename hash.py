import hashlib

password = input("Enter your password: ")

hashed = hashlib.sha256(password.encode()).hexdigest()
print(hashed)