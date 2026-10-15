# Run: python L1/TASK_2/extract_numbers.py "abc 12 3.5 7"

import argparse
import re


def extract_numbers(text):
    float_list = []
    odd_list = []
    even_list = []

    for token in re.findall(r"\d+\.\d+|\d+", text):
        if "." in token:
            float_list.append(float(token))
        elif int(token) % 2 == 0:
            even_list.append(int(token))
        else:
            odd_list.append(int(token))

    return float_list, odd_list, even_list


def main():
    parser = argparse.ArgumentParser(
        description="Extract floats, odd and even integers from a string."
    )
    parser.add_argument("text", help="String to extract numbers from")
    args = parser.parse_args()

    float_list, odd_list, even_list = extract_numbers(args.text)

    print(f"floatList: {float_list}")
    print(f"oddList: {odd_list}")
    print(f"evenList: {even_list}")


main()
