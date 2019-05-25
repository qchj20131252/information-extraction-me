"""
This module to generate vocabulary list
"""

import random
import os
import codecs
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')


def load_char_file(f_input):
    """
    Get all char in files
    :param string: input file
    """
    file_char = {}
    with codecs.open(f_input, 'r', 'utf-8') as fr:
        for line in fr:
            try:
                dic = json.loads(line.decode('utf-8').strip())
                sentence = dic['text']
                for c in sentence:
                    file_char[c] = file_char.get(c, 0) + 1
            except:
                continue

    return file_char


def get_char(train_file, dev_file):
    """
    Get vocabulary file from the field 'postag' of files
    :param string: input train data file
    :param string: input dev data file
    """
    char_dic = load_char_file(train_file)
    if len(char_dic) == 0:
        raise ValueError('The length of train char is 0')
    dev_char_dic = load_char_file(dev_file)
    if len(dev_char_dic) == 0:
        raise ValueError('The length of dev word is 0')
    for c in dev_char_dic:
        if c in char_dic:
            char_dic[c] += dev_char_dic[c]
        else:
            char_dic[c] = dev_char_dic[c]
    print '<UNK>'
    char_set = set()
    value_list = sorted(char_dic.iteritems(), key=lambda d: d[1], reverse=True)
    for word in value_list:
        print word[0]
        char_set.add(word[0])

    # add predicate in all_50_schemas
    if not os.path.exists('./data/all_50_schemas'):
        raise ValueError("./data/all_50_schemas not found.")
    with codecs.open('./data/all_50_schemas', 'r', 'utf-8') as fr:
        for line in fr:
            dic = json.loads(line.decode('utf-8').strip())
            p = dic['predicate']
            for p_char in p:
                if p_char not in char_set:
                    char_set.add(p)
                    print p


if __name__ == '__main__':
    train_file = sys.argv[1]
    dev_file = sys.argv[2]
    get_char(train_file, dev_file)