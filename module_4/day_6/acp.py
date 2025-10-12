import random
import string

def generate_random_password(length=12):
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    password_list = list(password)
    random.shuffle(password_list)
    shuffled_password = ''.join(password_list)
    return shuffled_password

random_password = generate_random_password()
print(random_password)