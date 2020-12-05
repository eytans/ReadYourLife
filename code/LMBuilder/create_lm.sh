#!/bin/bash

# run with 1 paramater to crreate LM.
# 1. wiki page subject
# 2. if exists then range

range=${2}
if [[ -z ${range} ]]; then
	range=3
fi

fixed_name=`echo ${1} | tr ' ' '_'`_r${range}
errors_text=${fixed_name}.txt

# create a subjected wiki file
subjected_wiki=${fixed_name}_wiki
python3 ./scripts/create_wiki_on_subject.py -r ${range} -o ${subjected_wiki} ../resources/enwiki-latest-pages-articles.xml ./titles.p "$1"

# clean wiki with java program
clean_text=${fixed_name}_clean_text 
java -Didea.launcher.port=7533 -Didea.launcher.bin.path=/home/eytan.s/apps/idea-IC-143.1821.5/bin -Dfile.encoding=UTF-8 -classpath /usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/lib/charsets.jar:/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/lib/compilefontconfig.jar:/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/lib/ext/dnsns.jar:/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/lib/ext/icedtea-sound.jar:/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/lib/ext/java-atk-wrapper.jar:/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/lib/ext/localedata.jar:/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/lib/ext/sunjce_provider.jar:/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/lib/ext/sunpkcs11.jar:/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/lib/ext/zipfs.jar:/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/lib/javazic.jar:/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/lib/jce.jar:/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/lib/jsse.jar:/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/lib/management-agent.jar:/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/lib/resources.jar:/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/lib/rhino.jar:/usr/lib/jvm/java-1.7.0-openjdk-amd64/jre/lib/rt.jar:/home/eytan.s/work/readyourlife/code/LMBuilder/libs/WikiToText/build/classes/main:/home/eytan.s/work/readyourlife/code/LMBuilder/libs/WikiToText/build/resources/main:/home/eytan.s/work/readyourlife/code/LMBuilder/libs/bliki-core-3.0.19.jar:/home/eytan.s/work/readyourlife/code/LMBuilder/libs/commons-compress-1.10.jar:/home/eytan.s/apps/idea-IC-143.1821.5/lib/idea_rt.jar com.intellij.rt.execution.application.AppMain com.eytan.wiki2text.Wikipedia2Txt ${subjected_wiki} > ${clean_text} 2> ${errors_text}

## format text to fit cmu (add <s> and </s>)
#formated_clean_text=${1}_formated_clean_text
#cat ${clean_text} | sed 's/^/ <s> /' | sed 's/$/ <\/s> /' > ${formated_clean_text}

# create corpus file
corpus_file=${fixed_name}_corpus
cat ${clean_text} | ./scripts/tocorpus.pl | tr "-" " " > ${corpus_file}

# create vocabulary
vocab=${fixed_name}.vocab
./scripts/mkvocab.pl < ${corpus_file} > ${vocab}

# for explanation please see: http://www.cs.brandeis.edu/~cs114/CS114_docs/SRILM_Tutorial_20080512.pdf

# create ngram count file
ngram_count=${fixed_name}_ngram.count
../resources/srilm/bin/i686-m64/ngram-count -vocab ${vocab} -text ${corpus_file} -write ${ngram_count} -unk

# create language model
lm=${fixed_name}.lm
../resources/srilm/bin/i686-m64/ngram-count -vocab ${vocab} -read ${ngram_count} -lm ${lm} -gt1min 3 -gt1max 7 -gt2min 3 -gt2max 7 -gt3min 3 -gt3max 7

