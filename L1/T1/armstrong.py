# Run: python L1/T1/armstrong.py

import argparse


def is_armstrong(number):
    digits = str(number)
    return number == sum(int(digit) ** len(digits) for digit in digits)


def recursive_sum(numbers):
    if not numbers:
        return 0
    return numbers[0] + recursive_sum(numbers[1:])


def main():
    argparse.ArgumentParser(
        description="Find Armstrong numbers between 9 and 9999 and sum them."
    ).parse_args()

    armstrong_numbers = [n for n in range(9, 10000) if is_armstrong(n)]

    print("Armstrong numbers:")
    for number in armstrong_numbers:
        print(number)

    print(f"Sum: {recursive_sum(armstrong_numbers)}")


main()
