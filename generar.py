import random
import string


def generate_serie(start_number):
    prefix = ''.join(random.choices(string.ascii_uppercase, k=5))
    number = str(start_number).zfill(3)
    code = f"00{prefix}-{number}"
    return code


start_number = 1

code = generate_serie(start_number)
print(code)
