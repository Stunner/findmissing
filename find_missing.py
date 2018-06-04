import sys
import argparse
import os
import re

# Works with:
# cat ~/Desktop/gdrive.txt | python3 ~/Dropbox/Programming/Projects/Open\ Source/find_missing/find_missing.py -p 'DSC004.(\d\d\d)' -l DSC004.099

# TODO: determine if strings are ascending or descending and emit error as soon as an unordered string is encountered and stop prematurely rather than have script output erroneous values

class G:
    verbose_opt = False

# reference: https://stackoverflow.com/a/11541450/347339
def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle

def process_args(args):
    parser = argparse.ArgumentParser(description="Takes a list of SORTED strings matching a specified pattern and outputs what is missing.")

    parser.add_argument('--file', '-f', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--pattern', '-p', help='[P]attern specified with regex and a single group' 
                                                'that refers to the portion of the string that has numbers.', required=True, nargs="?", default=None)
    parser.add_argument('--first', '-i', help='F[i]rst string name that is expected to exist. This script will count missing strings from it.', default='0')                                            
    parser.add_argument('--last', '-l', help='[L]ast string name that is expected to exist. This script will count missing strings up to it.')
    parser.add_argument('--verbose', '-v', help='Prints events to STDOUT.', action='store_true')
    args = parser.parse_args()
    G.verbose_opt = args.verbose
    return args, parser

def main(args):
    args, parser = process_args(args)
    pattern_str = re.compile(args.pattern)
    last_match = None
    if args.last:
        last_match = re.search(pattern_str, args.last)
        if not last_match:
            raise parser.error("Value provided for last must be findable by provided pattern regex."
            "\nLast provided: " + args.last + "\nRegex provided: " + args.pattern)
    
    last_seen = -1
    while True:
        line = args.file.readline()
        if not line:
            break
        
        matches = re.search(pattern_str, line)
        if matches:
            try:
                iterable_str = matches.group(1)
            except IndexError as exception:
                raise parser.error("Regex provided in pattern must have group denoting iterable portion of string.")
            else:
                # print('itr str: ' + iterable_str)
                iterable_num = int(iterable_str)
                # print('itr num: ' + str(iterable_num))
                difference = iterable_num - last_seen
                if difference > 1:
                    for i in range(difference - 1):
                        last_seen += 1
                        print(str(last_seen))
                last_seen = iterable_num
    
    # Print strings up to last param.
    if last_match:
        iterable_str = last_match.group(1)
        difference = int(iterable_str) - last_seen
        if difference > 1:
            for i in range(difference):
                last_seen += 1
                print(str(last_seen))

if __name__ == '__main__':
    main(sys.argv)