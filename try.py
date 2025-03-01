'''
import random


def get_number(type):
    return f"Your {type} number is: {random.randint(1, 100)}"

if __name__ == "__main__":
    print(get_number("lucky"))
    print(get_number("unlucky"))
'''
import random

print("Your lucky number is:", random.randint(1, 100))
print("Your unlucky number is:", random.randint(1, 100))

