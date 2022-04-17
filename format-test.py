#!/usr/bin/env python3

###
### CS 21 Concurrent Programming
### Spring 2022
### Project: Wordle with Friends
### format-test.py:
###     Test Format class
### 

from Format import Format

def equal(got, expected):
    """ check if two things are equal """
    return got == expected

def __test_print_helper(format_instance, description, expected, WORD, correct, semi_correct):
    """ helper function for printing tests """
    print('Testing %s: %s' % (WORD, description))
    result = format_instance.format_string(WORD, correct, semi_correct)
    print(result)

    ok = equal(expected, result)

    if ok:
        print("\033[32m Test passed. \033[0m")
    else:
        print("\033[31m Test failed! \033[0m")
    
    return ok

def test_format(format_instance):
    """ tests for formatting """
    WORD = 'party'

    print("\n...Testing formating...\n")
    
    __test_print_helper(format_instance, 'none correct', WORD, WORD, [], [])
    __test_print_helper(format_instance,
                        'first letter correct',
                        '\033[32mp\033[0marty',
                        WORD, [0], [])
    __test_print_helper(format_instance,
                        'two letters next to each other correct',
                        '\033[32mp\033[0m\033[32ma\033[0mrty',
                        WORD, [0, 1], [])
    __test_print_helper(format_instance,
                        'two letters next to each other correct',
                        '\033[32mp\033[0mar\033[32mt\033[0my',
                        WORD, [0, 3], [])
    __test_print_helper(format_instance,
                        'all correct',
                        '\033[32mp\033[0m\033[32ma\033[0m\033[32mr\033[0m\033[32mt\033[0m\033[32my\033[0m',
                        WORD, [0, 1, 2, 3, 4], [])
    __test_print_helper(format_instance,
                        'first letter semi-correct',
                        '\033[93mp\033[0marty',
                        WORD, [], [0])
    __test_print_helper(format_instance,
                        'some semi-correct',
                        '\033[93mp\033[0ma\033[93mr\033[0mty',
                        WORD, [], [0, 2])
    __test_print_helper(format_instance,
                        'all semi-correct',
                        '\033[93mp\033[0m\033[93ma\033[0m\033[93mr\033[0m\033[93mt\033[0m\033[93my\033[0m',
                        WORD, [], [0, 1, 2, 3, 4])

def __test_error_helper(format_instance, description, WORD, correct, semi_correct):
    """ helper function for error tests """
    print(f'Testing correct: {correct}, semi-correct: {semi_correct} %s' % description)

    try:
        format_instance.format_string(WORD, correct, semi_correct)
        print("\033[31m Test failed! \033[0m")
    except ValueError:
        print("\033[32m Test passed. \033[0m")

def test_errors(format_instance):
    """ tests for error cases """
    WORD = 'idkkk'

    print("\n...Testing error handling...\n")

    __test_error_helper(format_instance,
                        'raises exception',
                        WORD,
                        [0, 1, 4, 5, 6, 7, 2],
                        [])
    __test_error_helper(format_instance,
                        'raises exception',
                        WORD,
                        [],
                        [0, 1, 4, 5, 6, 3])
    __test_error_helper(format_instance,
                        'raises exception',
                        WORD,
                        [0, 1, 4, 5, 6, 7, 2],
                        [0, 1, 4, 5, 6, 3])

def main():
    test = Format()

    test_format(test)
    test_errors(test)

if __name__ == '__main__':
    main()

    exit(0)
