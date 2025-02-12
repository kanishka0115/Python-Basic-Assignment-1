# Q2. Write a Python program that generates a password with the following conditions:
# At least one uppercase letter.
# At least one lowercase letter.
# At least two numbers.
# At least one special character (e.g., !@#$%&*).
# The password should be exactly 16 characters long.
# The password should contain no repeating characters.
# The password should have a random order each time.

import random
import string

def generate_password():
    uppercase = list(string.ascii_uppercase) 
    lowercase = list(string.ascii_lowercase)  
    digits = list(string.digits) 
    special_chars = list("!@#$%&*")


    password_chars = [
        random.choice(uppercase), 
        random.choice(lowercase), 
        random.choice(digits), 
        random.choice(digits),
        random.choice(special_chars)
    ]

    all_chars = uppercase + lowercase + digits + special_chars
    while len(password_chars) < 16:
        char = random.choice(all_chars)
        if char not in password_chars:  
            password_chars.append(char)


    random.shuffle(password_chars)
    

    return "".join(password_chars)


print(generate_password())