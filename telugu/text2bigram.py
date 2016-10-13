#! /usr/bin/python3
import re
import sys
from collections import defaultdict, Counter

if len(sys.argv) < 2:
    print("""Usage: {0} input_text_file [show_bigram]
    Program counts the frequency of each Telugu letter following another and 
    writes out a binary <input_text_file>.bigram using pickle.
    [show_bigram] - when supplied a text file with the bigram is shown.
    """.format(sys.argv[0]))
    sys.exit()

#                            ↓ include space also.
aksh_pattern = re.compile(r"( )|([ఁ-ఔ])|(([క-హ]్)*[క-హ][ా-ౌ])|"
                          r"(([క-హ]్)*[క-హ](?![ా-్]))|(([క-హ]్)+(?=\s))")
bicount = defaultdict(Counter)
unicount = Counter()
beg_line = "^"
end_line = "$"

# Build the dictionaries
dump = open(sys.argv[1])
for line in dump:
    prev_akshara = beg_line
    for aksh_match in aksh_pattern.finditer(line):
        akshara = aksh_match.group()
        bicount[prev_akshara][akshara] += 1
        unicount[prev_akshara] += 1
        prev_akshara = akshara
    unicount[prev_akshara] += 1
    bicount[prev_akshara][end_line] += 1
dump.close()

# Dump Pickle
import pickle
with open(sys.argv[1]+'.bigram', 'wb') as f:
    pickle.dump((beg_line, end_line, unicount, bicount), f, 2)     

# DUMP
if len(sys.argv) < 3:
    sys.exit()

fout = open('/tmp/bigram.txt', 'w')  
for key, n in sorted(unicount.items(), key=lambda x: x[1], reverse=True):
    fout.write("\n\n" + key + " : " + str(n) + "\n ")
    for char, count in sorted(bicount[key].items(), 
                              key=lambda x: x[1],
                              reverse=True):
        fout.write(" "+char+":"+str(count))
fout.close()

import os
os.system('gedit /tmp/bigram.txt &')