import os
import argparse
from time import time
from scripts import cleaner as cl
from time import gmtime as get_time
from time import strftime as format_time


#Create Parser
my_parser = argparse.ArgumentParser(description='Data Cleaner Interface')

# Add the arguments
my_parser.add_argument('input',
                       metavar='input',
                       type=str,
                       help='the dir with data to clean')
my_parser.add_argument('-o',
                       '--output',
                       action='store',
                       help='siefy the path to output dir')
my_parser.add_argument('-l',
                       '--locations',
                       action='store',
                       help='set locations file')
my_parser.add_argument('-p',
                       '--print',
                       action='store_true',
                       help='print summary results to console')
my_parser.add_argument("-na",
                       "--notappend",
                       action='store_true',
                       help='do not append cleaned results to master file')

# Execute parse_args()
args = my_parser.parse_args()

if not args.output and not args.locations and os.path.isdir(args.input):
    cleaner = cl.Cleaner(args.input)
    if not os.path.exists('output'): os.mkdir('output')

elif args.output and not args.locations and os.path.isdir(args.input):
    cleaner = cl.Cleaner(args.input, args.output)

elif args.output and args.locations and os.path.isdir(args.input):
    cleaner = cl.Cleaner(args.input, args.output, args.locations)

else:
    cleaner = cl.Cleaner()
    if not os.path.exists('output'): os.mkdir('output')

if args.print:
    cleaner.on_print()

if args.notappend:
    cleaner.off_append()

print("Reading files in", os.getcwd() + '\\' +args.input)
start = time()
cleaner.start_clean()
end = time()
print("Cleaning complete\nTime Elapsed: ", format_time("%H:%M:%S", get_time(end - start)))
print("Cleaned files were sent to ", end="")

if args.output:
    print(os.getcwd() + '\\' + args.output)
else:
    print(os.getcwd() + '\output')
