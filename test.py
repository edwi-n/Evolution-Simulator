def verify(number):
    if (number == 1):
        return False
    for i in range(2, number):
        if i*i > number:
            return True
        if (number % i == 0):
            return False
    return True


print(verify(101))
