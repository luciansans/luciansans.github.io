# do calculation to determine if prime 
def is_prime(n):
    if n < 2:
        return False

    for x in range(2, int(n ** 0.5) + 1):
        if n % x == 0:
            return False

    return True

# Prompt the user to enter the number
n = int(input("Enter a number: "))

# Check if the number is prime and print the outcome
if is_prime(n):
    print(n, "is a prime number.")
else:
    print(n, "is not a prime number.")