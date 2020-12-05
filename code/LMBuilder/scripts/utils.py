import sys
__author__ = 'eytan'

DEBUG = True


def normal_print(text, stream=None):
    if stream is None:
        text = text.encode()
        stream = sys.stdout.buffer
    error_print(text, stream)


def error_print(text, stream=None):
    if stream is None:
        stream = sys.stderr.buffer
        text = text.encode()
    stream.write(text)
    stream.flush()


def debug_print(text, stream=None):
    if DEBUG:
        if stream is None:
            stream = sys.stdout.buffer
            text = text.encode()
        stream.write(text)
        stream.flush()