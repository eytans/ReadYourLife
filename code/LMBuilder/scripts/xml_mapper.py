import utils
import sys
import argparse
import functools

__author__ = 'eytan'

args_parser = argparse.ArgumentParser(description='Create an index for wiki dump')
args_parser.add_argument('dump', action='store', help='path to wiki dump file')
args_parser.add_argument('--outfile', '-o', action='store', default=None, help='file to write output too')
args_parser.add_argument('--debug-start', action='store', type=int, default=0, help='start creating mapping from here')
args_parser.add_argument('--debug-end', action='store', type=int, default=-1, help='stop mapping here')
args_parser.add_argument('--debug-out', action='store', default=None, help='print debug data here')

args = args_parser.parse_args(sys.argv[1:])
debug_start = args.debug_start
debug_end = args.debug_end

if args.debug_out is not None:
    debug_stream = open(args.debug_out, 'w', encoding='utf-8')
else:
    debug_stream = sys.stdout.buffer

if args.outfile is not None:
    output_stream = open(args.outfile, 'w', encoding='utf-8')
else:
    output_stream = sys.stdout.buffer


def line_to_size(text):
    return len(text.encode('utf-8'))
    
dump_path = args.dump
with open(dump_path, 'r', encoding="utf-8") as dump:
    dump.seek(debug_start)
    line = " "
    start = 0
    title = " "
    while line:
        start = dump.tell()
        line = dump.readline()
        if u"<page>" in line:
            page = [line]
            page_start = start
            if not line.strip().startswith(u"<page>"):
                utils.debug_print(line, stream=debug_stream)
            while u"</page>" not in line:
                line = dump.readline()
                page.append(line)
                if u"<title" in line:
                    title = line.split('>')[1].split('<')[0]
            if not line.endswith(u"</page>\n"):
                utils.debug_print(line, stream=debug_stream)
            page_len = functools.reduce(lambda x, y: x+len(y), page, 0)
            utils.normal_print(title + " - " + str(page_start) + " - " + str(page_len) + '\n', stream=output_stream)
            if debug_end != -1 and debug_end <= dump.tell():
                utils.debug_print('\n ending Diffrence for debug, page end: ' + str(dump.tell()) + ' debug end:' +
                                  str(debug_end), stream=debug_stream)
                break

#
# i = 0
# mapping.close()
# mapping = open('mapping.txt', 'r', encoding='utf8')
# for line in mapping.readlines():
# if i > 20:
# break
# line_a = line.split('-')
# start = (int(line_a[-2].strip()))
# end = int(line_a[-1].strip().replace(u'\n', ''))
# line = data.readline()
# if line.strip().replace(u'\n', '') != u'<page>':
# print('shit bad line at start ' + str(start) + line)
# i += 1
# data.seek(end - 8)
# if data.readline() != u'</page>\n':
# print('shit bad line at end ' + str(end) + ' ' + line)
# i += 1
