import sys
import re

''' param 1 path to srt
param 2 path to out'''
def foo(srt_path, out_path):

    srt_file = open(srt_path, 'r')
    srt = " ".join(srt_file.readlines())
    srt = re.sub(r'[0-9]{1,3}:[0-9]{1,3}:[0-9]{1,3}[.,][0-9]{1,3}\s*(-->|,)\s*[0-9]{1,3}:[0-9]{1,3}:[0-9]{1,3}[.,][0-9]{1,3}', '', srt)
    srt = re.sub(r'\n\s*[0-9]+\s*\n', ' ', srt)
    srt = re.sub(r'^\s*[0-9]+\s*\n', '', srt)

    if out_path is not None:
      out_file = open(out_path, 'w')
      out_file.write(srt)
    else:
      print(srt)
