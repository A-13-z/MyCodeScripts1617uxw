import random, string
def generate(length, chars = string.ascii_letters + string.digits + string.punctuation):
    print(''.join(random.choice(chars) for _ in range(length)))

generate(length = int(input('Enter the length of your password: ')))
