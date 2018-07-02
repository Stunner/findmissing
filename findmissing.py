from __future__ import print_function
import sys
import argparse
import re
import io


# TODO: Allow for ranges of missing numbers (i.e. 22-45 54-56 72 73 75) to be displayed instead of listing out all
# missing numbers which can be tedious to digest when printed individually

class G:
    parser = None
    last_match_int = None


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
    args = parser.parse_args(args[1:])
    return args, parser


def asc_or_desc_check(num1, num2, asc_or_desc=0):
    asc_or_desc_val = asc_or_desc
    if num2 > num1:  # ascending
        if asc_or_desc_val == 0:
            asc_or_desc_val = 1
        else:  # already set
            if asc_or_desc_val == -1:
                raise Exception("Iterable string input must be sorted!"
                                "\nLast saw: " + str(num1) +
                                "\nNow see: " + str(num2))
    else:  # descending
        if asc_or_desc_val == 0:
            asc_or_desc_val = -1
        else:  # already set
            if asc_or_desc_val == 1:
                raise Exception("Iterable string input must be sorted!"
                                "\nLast saw: " + str(num1) +
                                "\nNow see: " + str(num2))
    return asc_or_desc_val


def get_specified_num(pattern, line):
    matches = re.search(pattern, line)
    iterable_str = None
    if matches:
        try:
            iterable_str = matches.group(1)
        except IndexError as exception:
            raise AttributeError("Regex provided in pattern must have group (specified with parenthesis) denoting "
                                 "iterable portion of string.")
    if iterable_str:
        try:
            iterable_num = int(iterable_str)
        except TypeError as exception:
            raise TypeError("Regex provided in pattern must have numeric values denoting iterable portion of string.")
        except ValueError as exception:
            raise ValueError("Regex provided in pattern must have numeric values denoting iterable portion of string.")
        else:
            return iterable_num
    return None


def calc_diff(asc_or_des, iterable_num, last_seen):
    diff = iterable_num - last_seen
    if asc_or_des == -1:
        diff = last_seen - iterable_num
    return diff


def print_last_seen(last_seen):
    # reference: https://stackoverflow.com/a/12028682/347339
    try:  # Python 2.7 compatibility
        with io.BytesIO(str(last_seen)) as file:
            s = file.read()
            try:
                print(s)
            except TypeError as exception:
                u = unicode(s, "utf-8")
                print(u)
    except TypeError as exception:
        print(last_seen)


def print_diff(diff, asc_or_desc, last_seen, stop_early):
    if last_seen == -1:
        # Assume we are ascending if last_seen hasn't been set,
        # as this can happen when first param is provided with value 0.
        asc_or_desc = 1

    for j in range(diff - stop_early):
        if asc_or_desc == 0:
            if last_seen == 0:
                # assume ascending as last seen should never be decremented to -1
                asc_or_desc = 1

        if asc_or_desc == 1:
            last_seen = last_seen + 1
        else:
            last_seen = last_seen - 1
        if G.last_match_int is not None and G.last_match_int < last_seen:
            return True  # stop reading as soon as we get to last number
        print_last_seen(last_seen)
    return False


def main(args):
    args, G.parser = process_args(args)
    pattern_str = re.compile(args.pattern)
    last_match = None
    last_seen = -1
    prev_itr_num = -1
    if args.last:
        last_match = re.search(pattern_str, args.last)
        if not last_match:
            raise G.parser.error("Value provided for last must be findable by provided pattern regex."
                                 "\nLast provided: " + args.last + "\nRegex provided: " + args.pattern)
        else:
            last_match_str = last_match.group(1)
            G.last_match_int = int(last_match_str)
    first_expected = None
    if args.first:
        first_match = re.search(pattern_str, args.first)
        if not first_match:
            raise G.parser.error("Value provided for first must be findable by provided pattern regex."
                                 "\nLast provided: " + args.first + "\nRegex provided: " + args.pattern)
        else:
            first_expected = int(first_match.group(1))

    ascend_or_descend = 0
    difference = 0
    aborted = False
    i = -1
    while True:
        i += 1
        line = args.file.readline()
        if not line:
            break

        iterable_num = get_specified_num(pattern_str, line)
        if iterable_num is not None:
            if i > 0:
                ascend_or_descend = asc_or_desc_check(prev_itr_num, iterable_num, ascend_or_descend)

            if i == 0 and first_expected is not None:
                difference = iterable_num - first_expected
                stop_early = 0
                if first_expected > 0:
                    last_seen = first_expected - 1
            elif last_seen != -1:
                difference = calc_diff(ascend_or_descend, iterable_num, last_seen)
                stop_early = 1
            if difference < 0:  # keep reading until we get to first expected number
                continue
            elif difference > 1:
                aborted = print_diff(difference, ascend_or_descend, last_seen, stop_early)
                if aborted:
                    break
            elif difference == 1 and i == 0 and first_expected is not None:
                aborted = print_diff(difference, ascend_or_descend, last_seen, stop_early)
                if aborted:
                    break
            prev_itr_num = iterable_num
            last_seen = iterable_num
    args.file.close()

    # Print strings up to last param.
    if last_match and not aborted:
        iterable_str = last_match.group(1)
        difference = int(iterable_str) - last_seen
        if difference > 0:
            for i in range(difference):
                last_seen += 1
                print(str(last_seen))


if __name__ == '__main__':
    main(sys.argv)
