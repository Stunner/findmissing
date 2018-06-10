import sys
import argparse
import os
import re

# Works with:
# cat ~/Desktop/gdrive.txt | python3 ~/Dropbox/Programming/Projects/Open\ Source/find_missing/find_missing.py -p
# 'DSC004.(\d\d\d)' -l DSC004.099

# TODO: determine if strings are ascending or descending and emit error as soon as an unordered string is 
# encountered and stop prematurely rather than have script output erroneous values

#TODO: have the first and last params cause output to "stop short" despite more valid iterable strings being present. 
# Comes in handy during subset inspection.

class G:
    verbose_opt = False
    parser = None

# reference: https://stackoverflow.com/a/11541450/347339
def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle

def process_args(args):
    parser = argparse.ArgumentParser(description="Takes a list of SORTED strings matching a specified"
                                                 "pattern and outputs what is missing.")

    parser.add_argument('--file', '-f', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--pattern', '-p', help='[P]attern specified with regex and a single group' 
                                                'that refers to the portion of the string that has numbers.',
                        required=True, nargs="?", default=None)
    parser.add_argument('--first', '-i', help='F[i]rst string name that is expected to exist.'
                                              ' This script will count missing strings from it.')
    parser.add_argument('--last', '-l', help='[L]ast string name that is expected to exist.'
                                             ' This script will count missing strings up to it.')
    parser.add_argument('--verbose', '-v', help='Prints events to STDOUT.', action='store_true')
    args = parser.parse_args()
    G.verbose_opt = args.verbose
    return args, parser


def asc_or_desc_check(num1, num2, asc_or_desc=0):
    # print("iterable num: " + str(iterable_num) + " last seen: " + str(last_seen))
    asc_or_desc_val = 0
    if num2 > num1:  # ascending
        if asc_or_desc == 0:
            asc_or_desc_val = 1
        else:  # already set
            if asc_or_desc == -1:
                raise Exception("Iterable string input must be sorted!"
                                "\nLast saw: " + str(num1) +
                                "\nNow see: " + str(num2))
    else:  # descending
        if asc_or_desc == 0:
            asc_or_desc_val = -1
        else:  # already set
            if asc_or_desc == 1:
                raise Exception("Iterable string input must be sorted!"
                                "\nLast saw: " + str(num1) +
                                "\nNow see: " + str(num2))
    return asc_or_desc_val


def init_asc_or_desc_check(pattern, file):
    # TODO: fix this assumption that 2 lines will always exist...
    line = file.readline()
    num1 = get_specified_num(pattern, line)
    line = file.readline()
    num2 = get_specified_num(pattern, line)
    file.seek(0) # reset to beginning of file
    return asc_or_desc_check(num1, num2)


def get_specified_num(pattern, line):
    matches = re.search(pattern, line)
    iterable_str = None
    if matches:
        try:
            iterable_str = matches.group(1)
        except IndexError as exception:
            raise G.parser.error("Regex provided in pattern must have group denoting iterable portion of string.")
    if iterable_str:
        try:
            iterable_num = int(iterable_str)
        except TypeError as exception:
            raise G.parser.error("Regex provided in pattern must have numeric values denoting iterable portion of string.")
        else:
            return iterable_num
    return None


def calc_diff(asc_or_des, iterable_num, last_seen):
    diff = iterable_num - last_seen
    if asc_or_des == -1:
        diff = last_seen - iterable_num
    return diff


def main(args):
    print(args)
    args, G.parser = process_args(args)
    pattern_str = re.compile(args.pattern)
    last_match = None
    last_seen = -1
    if args.last:
        last_match = re.search(pattern_str, args.last)
        if not last_match:
            raise parser.error("Value provided for last must be findable by provided pattern regex."
            "\nLast provided: " + args.last + "\nRegex provided: " + args.pattern)
    first_match = None
    first_expected = None
    if args.first:
        first_match = re.search(pattern_str, args.first)
        if not first_match:
            raise parser.error("Value provided for first must be findable by provided pattern regex."
            "\nLast provided: " + args.first + "\nRegex provided: " + args.pattern)
        else:
            first_expected = int(first_match.group(1))
            print("first expected: " + str(first_expected))
    
    ascend_or_descend = init_asc_or_desc_check(pattern_str, args.file)
    while True:
        line = args.file.readline()
        if not line:
            break

        iterable_num = get_specified_num(pattern_str, line)
        if iterable_num is not None:

            difference = calc_diff(ascend_or_descend, iterable_num, last_seen)
            if first_expected:
                difference = iterable_num - first_expected
            if difference > 1:
                for i in range(difference - 1):
                    if ascend_or_descend == 1:
                        last_seen = last_seen + 1
                    else:
                        last_seen - 1
                    print(str(last_seen))
            last_seen = iterable_num

        # matches = re.search(pattern_str, line)
        # if matches:
        #     try:
        #         iterable_str = matches.group(1)
        #     except IndexError as exception:
        #         raise parser.error("Regex provided in pattern must have group denoting iterable portion of string.")
        #     else:
        #         # print('itr str: ' + iterable_str)
        #         iterable_num = int(iterable_str)
        #         #asc or descend check
        #         if last_seen != -1:
        #             # print("iterable num: " + str(iterable_num) + " last seen: " + str(last_seen))
        #             if iterable_num > last_seen: #ascending
        #                 if ascend_or_descend == 0:
        #                     ascend_or_descend = 1
        #                 else: #already set
        #                     if ascend_or_descend == -1:
        #                         raise Exception("Iterable string input must be sorted!"
        #                         "\nLast saw: " + str(last_seen) +
        #                         "\nNow see: " + str(iterable_num))
        #             else: #descending
        #                 if ascend_or_descend == 0:
        #                     ascend_or_descend = -1
        #                 else: #already set
        #                     if ascend_or_descend == 1:
        #                         raise Exception("Iterable string input must be sorted!"
        #                         "\nLast saw: " + str(last_seen) +
        #                         "\nNow see: " + str(iterable_num))
                # print('itr num: ' + str(iterable_num))
    
    # Print strings up to last param.
    if last_match:
        iterable_str = last_match.group(1)
        difference = int(iterable_str) - last_seen
        if difference > 1:
            for i in range(difference):
                last_seen += 1
                print(str(last_seen))
    # Print strings up from first param.
    if first_match:
        iterable_str = first_match.group(1)
        difference = last_seen - int(iterable_str)
        if difference > 1:
            for i in range(difference):
                last_seen -= 1
                print(str(last_seen))


if __name__ == '__main__':
    main(sys.argv)