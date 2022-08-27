import sys
import codecs
import os
import math
import operator
import json
import argparse
from functools import reduce

def generate_translated(path,filename):
    f = open(path,encoding = "utf-8")
    text = f.read()
    sen = text.split("\n")
    result = list()
    for sentence in sen:
        sentence = sentence.replace("<OOV>","@")
        sentence = sentence.replace(" ","")
        sentence = " ".join(sentence)
        #change @ back to <OOV>
        sentence = sentence.replace("@","<OOV>")
    #    print(sentence)
        result.append(sentence)
    #    print(sentence)
    #    break

    with open(filename,"a") as f:
        for sentence in result:
            f.write(str(sentence+"\n"))
        f.close()
    
def fetch_data(cand, ref):
    """ Store each reference and candidate sentences as a list """
    references = []
    reference_file = codecs.open(ref, 'r')
    references.append(reference_file.readlines())
        
    candidate_file = codecs.open(cand, 'r', 'utf-8')
    candidate = candidate_file.readlines()
    return candidate, references


def count_ngram(candidate, references, n):
    clipped_count = 0
    count = 0
    r = 0
    c = 0
    for si in range(len(candidate)):
        # Calculate precision for each sentence
        ref_counts = []
        ref_lengths = []
        # Build dictionary of ngram counts
        for reference in references:
            ref_sentence = reference[si]
            ngram_d = {}
            words = ref_sentence.strip().split()
            ref_lengths.append(len(words))
            limits = len(words) - n + 1
            # loop through the sentance consider the ngram length
            for i in range(limits):
                ngram = ' '.join(words[i:i+n]).lower()
                if ngram in ngram_d.keys():
                    ngram_d[ngram] += 1
                else:
                    ngram_d[ngram] = 1
            ref_counts.append(ngram_d)
        # candidate
        cand_sentence = candidate[si]
        cand_dict = {}
        words = cand_sentence.strip().split()
        limits = len(words) - n + 1
        for i in range(0, limits):
            ngram = ' '.join(words[i:i + n]).lower()
            if ngram in cand_dict:
                cand_dict[ngram] += 1
            else:
                cand_dict[ngram] = 1
        clipped_count += clip_count(cand_dict, ref_counts)
        count += limits
        r += best_length_match(ref_lengths, len(words))
        c += len(words)
    if clipped_count == 0:
        pr = 0
    else:
        pr = float(clipped_count) / count
    bp = brevity_penalty(c, r)
    return pr, bp


def clip_count(cand_d, ref_ds):
    """Count the clip count for each ngram considering all references"""
    count = 0
    for m in cand_d.keys():
        m_w = cand_d[m]
        m_max = 0
        for ref in ref_ds:
            if m in ref:
                m_max = max(m_max, ref[m])
        m_w = min(m_w, m_max)
        count += m_w
    return count


def best_length_match(ref_l, cand_l):
    """Find the closest length of reference to that of candidate"""
    least_diff = abs(cand_l-ref_l[0])
    best = ref_l[0]
    for ref in ref_l:
        if abs(cand_l-ref) < least_diff:
            least_diff = abs(cand_l-ref)
            best = ref
    return best


def brevity_penalty(c, r):
    if c > r:
        bp = 1
    else:
        bp = math.exp(1-(float(r)/c))
    return bp


def geometric_mean(precisions):
    return (reduce(operator.mul, precisions)) ** (1.0 / len(precisions))


def BLEU(candidate, references):
    precisions = []
    for i in range(4):
        pr, bp = count_ngram(candidate, references, i+1)
        precisions.append(pr)
    bleu = geometric_mean(precisions) * bp
    return bleu

if __name__=="main":
    
    parser = argparse.ArgumentParser(description='I am too lazy to add a description here. You wrote the code. You know what\'s it for')
    parser.add_argument('--path', help='path of machine translation file')
    parser.add_argument('--filename', help='path to save the generated file')
    parser.add_argument('--test',help='path to the standard translation')
    args = parser.parse_args()
    generate_translated(args.path,args.filename)
    candidate, references = fetch_data(args.test,args.filename)
    bleu = BLEU(candidate, references)
    print(bleu)
