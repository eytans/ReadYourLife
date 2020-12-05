#!/bin/bash

# for each weight create a new lm with w*LM1+(1-w)*LM2
if ! [ "$#" -eq 2 ]; then
  echo "need 2 params: LM1, LM2. exiting"
  exit 1
fi

for w in 10 20 30 40 50 60 70 80 90
do
  ../resources/srilm/bin/i686-m64/ngram -order 7 -lm "${1}"  -mix-lm "${2}" -lambda ${w} -write-lm merged_"${1}"_"${2}"_${w}.lm >merge_"${1}"_"${2}"_${w}.out 2>merge_"${1}"_"${2}"_${w}.error &
  ../resources/srilm/bin/i686-m64/ngram -order 7 -lm "${1}" -bayes 0 -mix-lm "${2}" -lambda ${w} -write-lm merged_"${1}"_"${2}"_${w}_bayes.lm >merge_"${1}"_"${2}"_${w}_bayes.out 2>merge_"${1}"_"${2}"_${w}_bayes.error &
done
