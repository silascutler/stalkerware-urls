#!/usr/bin/env python3

prog_ver  = "0.0.2"
prog_desc ='''Takes a list of domains, one per line, with # as the comment char
and convert it into a format that can be directly added to the pi-hole software

pi-hole is a DNS server implementation that blocks advertisers based on DNS list
pi-hole: https://github.com/pi-hole/pi-hole

© 2022 GI_Jack. Distrbuted under the GPLv3
https://www.gnu.org/licenses/gpl-3.0.txt


'''

config = {
    'null_addr' : "0.0.0.0"
}

output_header = '''# Title: StalkerwareDNS/Hosts
# Automaticly generated list of stalkerware DNS entries for the pi-hole
# https://github.com/GIJack/stalkerware-urls/blob/shove_it_in_your_pi-hole/shove_it_in_your_pi-hole.py
# pi-hole: https://github.com/pi-hole/pi-hole

'''

import sys
import argparse

class color:
    reset='\033[0m'
    bold='\033[01m'
    brightred='\033[95m'
    brightyellow='\033[93m'

def exit_with_error(exit_code,message):
    '''print error message to STDERR and exit with code'''
    out_message = "shoveit_in_your_pihole.py: " + color.brightred + "ERROR: " + color.reset + message
    print(out_message,file=sys.stderr)
    exit(exit_code)

def print_version_and_exit():
    out_message = prog_ver + "\t shove_it_in_your_pi-hole.py \t ©copyright 2022 GI_Jack, GPLv3"
    print(out_message)
    sys.exit(4)
    
def message(message):
    '''print formated message'''
    out_message = "shoveit_in_your_pihole.py: " + message
    print(out_message)
    
def warn(message):
    '''print a warning message'''
    out_message = "shoveit_in_your_pihole.py: " + color.brightyellow + "WARN: " + color.reset + message
    print(out_message,file=sys.stderr)

def strip_comments(in_lines):
    '''strip out comments and return list of lines. should be already converted to string with decode()'''
    comment   = "#"
    out_lines = []
    
    for line in in_lines:
        line = line.strip()
        if not line.startswith(comment) and line != "":
            out_lines.append(line.split(comment)[0])
            
    return out_lines

def convert_to_pihole(in_lines):
    '''convert each line to pi-hole format'''
    
    out_lines = []
    for line in in_lines:
        line = config['null_addr'] + " " + line
        out_lines.append(line)
    
    out_lines = "\n".join(out_lines)
    return out_lines

def get_lines_from_file(input_file):
    '''read the input file and return the lines as a list'''
    in_obj    = open(input_file,'r+')
    file_lines = in_obj.read()
    in_obj.close()

    file_lines = file_lines.split('\n')
    return file_lines

def write_output(out_lines,out_file):
    '''Write Output to File. takes two parameters, out_lines, and out_file'''
    try:
        out_obj  = open(out_file,'w')
    except:
        exit_with_error(1,"Could not write to output file: " + out_file + " Please check directory exists and permissions allow writing")

    file_out = output_header + '\n' + out_lines
    out_obj.write(file_out)
    out_obj.close()
        
def main():
    ## Parse input
    WARNS = 0
    parser = argparse.ArgumentParser(description=prog_desc,epilog="\n\n",add_help=False,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input_file_list", nargs="*"   , help="Input file(s) to Convert")
    parser.add_argument("-?","--help"             , help="Show This Help Message",action="help")
    parser.add_argument("-v","--version"          , help="Show version and quit",action="store_true")
    parser.add_argument("-o","--output"           , help="Output file. default block_list.pi_hosts",type=str)
    args = parser.parse_args()

    ## Sanity checks, and variable proccessing
    if args.version == True:
        print_version_and_exit()

    out_file = None
    if args.input_file_list == []:
        exit_with_error(2,"No input file(s) given, see --help")

    if args.output == None:
        out_file = "block_list.pi_hosts"
    else:
        out_file = args.output
        
    ## Alright, lets roll
    message("Proccessing file(s): " + " ".join(args.input_file_list))
    message("Writing Output to: " + out_file)
    out_lines = []
    for in_file in args.input_file_list:
        # Read from the input file
        try:
            in_lines  = get_lines_from_file(in_file)
        except:
            warn("Could not read file: " + input_file + " Please ensure this file exists and you have read permissions")
            WARNS += 1
            continue
        # Strip comments
        out_lines += strip_comments(in_lines)
        
    # Convert and add to list
    out_lines = convert_to_pihole(out_lines)
    # Write output
    write_output(out_lines,out_file)
main()
