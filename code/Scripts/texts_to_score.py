# compare two strings recieved as params

import sys
import difflib
import os
from wer.wer import justWer


def normalize_file_name(name):
    file_name = name.lower().replace(' ', '').replace('-', '').replace('_', '')
    return os.path.splitext(file_name)[0][:-4] + '.txt'


def compare_strings(seq1, seq2):
  sm = difflib.SequenceMatcher()
  sm.set_seqs(seq1, seq2)
  return sm.ratio()
  
 
def matching_word_count(lhs, rhs):
    lhs = lhs.split()
    rhs = rhs.split()
    count = 0
    for i, w in enumerate(lhs):
        if len(rhs) == i:
            break
        count += w == rhs[i]
    return count

def matching_word_count_percentage(lhs, rhs):
    if len(lhs) == 0:
      return -1
    lhs = lhs.split()
    rhs = rhs.split()
    count = 0
    for i, w in enumerate(lhs):
        if len(rhs) == i:
            break
        count += w == rhs[i]
    return (float(count)/len(lhs))*100

#def calc_wer(reference, hypothesis):
#    return wer.wer(reference, hypothesis)
    
def run_on_resources(path):
    print('path , default , custom, defult_w_count, custom_w_count , defult_w_count_percentage , custom_w_count_percentage , default_wer , default_wacc , custom_wer, custom_wacc')
    for d in os.listdir(path):
        d = os.path.join(path, d)
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if not f.endswith('.srt.res'):
                continue
            full_name = os.path.join(d, f)
            norm_name = normalize_file_name(f)
            cust_name = os.path.join(d, 'customout', norm_name)
            orig_text = open(full_name).read()
            custom_text = open(cust_name).read()
            cust_res = compare_strings(orig_text, custom_text)
            default_name = os.path.join(d, 'defaultout', norm_name)
            defult_text = open(default_name).read()
            default_res = compare_strings(orig_text, defult_text)
            default_w_c = matching_word_count(orig_text, defult_text)
            cust_w_c = matching_word_count(orig_text, custom_text)
            default_w_c_p = matching_word_count_percentage(orig_text, defult_text)
            cust_w_c_p = matching_word_count_percentage(orig_text, custom_text)
            default_wer = justWer(orig_text, defult_text)
            cust_wer = justWer(orig_text, custom_text)
            print(full_name + " , " + str(default_res) + ' , ' + str(cust_res)+ " , " + str(default_w_c) + ' , ' + str(cust_w_c) + ' , ' + str(default_w_c_p) + ' , ' + str(cust_w_c_p) + ' , ' + str(default_wer) + ' , ' + str(cust_wer)  )


if __name__ == '__main__':
  if len(sys.argv) < 3:
    exit()

  if sys.argv[1] == '-p':
    run_on_resources(sys.argv[2])
    exit()

  seq1 = sys.argv[1]
  seq2 = sys.argv[2]
  print(compare_strings(seq1, seq2))

