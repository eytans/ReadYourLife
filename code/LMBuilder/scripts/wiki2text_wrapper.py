#!/usr/bin/python
from subprocess import call
import sys
import argparse
import utils
import os


# build script for Wiki2Text
def build_wiki2text(project_folder='.', out=None, error=None):
    utils.normal_print("Working in dir: " + os.getcwd() + "\n")
    utils.normal_print("bilki in dir: " + os.getcwd() + '/' + project_folder + r'/libs/bliki-core-3.0.19.jar' + "\n")
    return call(['javac', '-d', project_folder + r'/bin/', '-cp', project_folder + r'/libs/commons-compress-1.10.jar;' +
                os.getcwd() + '/' + project_folder+r'/libs/bliki-core-3.0.19.jar;' + project_folder, project_folder +
                r'/src/com/eytan/wiki2text/Wikipedia2Txt.java'], stdout=out, stderr=error)


# run wiki2text
def run_wiki2text(path_to_wiki_xml, project_folder='.', out=None, error=None):
    return call(['java', '-cp', project_folder + r'/libs/commons-compress-1.10.jar:' + project_folder +
                 r'/libs/bliki-core-3.0.19.jar:' + project_folder + r'/src:' + project_folder + r'/bin;' +
                 project_folder, 'com.eytan.wiki2text.Wikipedia2Txt', path_to_wiki_xml])


def main():
    args_parser = argparse.ArgumentParser(description='Use java tool to translate wiki format to text')
    args_parser.add_argument('command', choices=['build', 'run', 'both'], help='command to run (build or run or both')
    args_parser.add_argument('--wiki_file', '-f', action='store', help='path to file of wiki dump format')
    args_parser.add_argument('--base', '-b', action='store', default='.', help='Base folder to work in')
    args_parser.add_argument('--outfile', '-o', action='store', default=None,
                             help='file to write output too')
    args_parser.add_argument('--errorfile', '-e', action='store', default=None,
                             help='file to write errors too')
    args = args_parser.parse_args(sys.argv[1:])
    # if len(sys.argv) < 2:
    #     print('usage: python wiki2text_wrapper.py {build | run | build run} <params>')
    #     print('build will compile the java class into project_folder/bin. optional param: LMBuilder_base="."')
    #     print('run will not build before running the class on the params, params = "path_to_a_wiki_xml [LMbuilder_base]"')
    #     print('build run will execute both one after the other with params for run')
    #     exit()
    project_folder = args.base
    command = args.command
    output = None
    if args.outfile is not None:
        output = open(args.outfile, 'w', encoding='utf-8')
    error_out = None
    if args.errorfile is not None:
        error_out = open(args.errorfile, 'w', encoding='utf-8')
    if command == 'build' or command == 'both':
        code = build_wiki2text(project_folder=project_folder, out=output, error=error_out)
        if code != 0:
            utils.error_print('Wiki2Text: build failed\n')
            exit(code)
    if command == 'run' or command == 'both':
        if args.wiki_file is None:
            utils.error_print('Wiki2Text: cant run without a wiki file\n')
            exit(1)
        path_to_wiki = args.wiki_file
        code = run_wiki2text(path_to_wiki, project_folder=project_folder, out=args.outfile, error=args.errorfile)
        if code != 0:
            utils.error_print('Wiki2Text: run error (in java tool)\n')
            exit(code)


if __name__ == '__main__':
    main()
