import hashlib

password = input("Enter your password: ")
hashed_password = hashlib.sha256(password.encode()).hexdigest()
print("Your hashed password is:", hashed_password)
