import re
import os
import sys

print("=== Major System ===")

script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
filename = os.path.join(script_dir, "IPA_words.txt")


def generate_regex(number_input, exclude_z_ending=False):

    # This is the original mapping... but you can define your own IPA. Total freedom!!!
    consonant_map = {
        '0': '[sz]',
        '1': '[tθdð]',
        '2': '[n]',
        '3': '[m]',
        '4': '[rɹɝ]',
        '5': '[lɫ]',
        '6': '(?:tʃ|dʒ|ʃ|ʒ)', # we want "dʒ" (same for "tʃ") to be seen as one unit, instead of "d" and "ʒ" being treated as two separate units.
        '7': '[kɡŋ]',
        '8': '[fv]',
        '9': '[pb]'
    }

    vowels = '[ˈˌhjwaeiouæəɛɪɔœøɒʌʊ]*' # list of vowels (to be ignored later)
    pattern = r'.*\t\/*' + vowels # final regex pattern

    for digit in number_input:
        if digit in consonant_map:
            pattern += consonant_map[digit] + vowels
        else:
            print(f"Invalid digit: {digit}")
            return None

    # Exclude entries that end with 'z' (to avoid the plural words)
    if exclude_z_ending:
        pattern += r'(?<!z)\/'
    else:
        pattern += r'\/'

    return pattern


def search_file(filename, regex_pattern):
    try:
        matches = []
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if re.match(regex_pattern, line):
                    matches.append(line)
        return matches
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


while True:
    number_input = input("\nEnter a number: ")

    exclude_option = input("Exclude IPAs ending with 'z' (to help with avoiding plural words)? (y/n): ").lower()
    exclude_z_ending = exclude_option == 'y' or exclude_option == 'yes'

    regex_pattern = generate_regex(number_input, exclude_z_ending)

    if regex_pattern:
        matches = search_file(filename, regex_pattern)

        if matches:
            print("\n\n")
            collated_words = '\n'.join(matches)
            print(collated_words)
        else:
            print("No matches found.")
