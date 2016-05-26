#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-03-23 13:17:29
# @Author  : Weizhong Tu (mail@tuweizhong.com)
# @Link    : http://www.tuweizhong.com
from __future__ import print_function
import os


def get_words(fname):
    with open(fname) as f:
        words = {line.strip() for line in f}
    return words


def main():
    my_words_f = 'my_words.txt'
    my_words = get_words(my_words_f)
    words_f = {x for x in os.listdir('.') if x.endswith('.txt')} - {my_words_f}

    all_words = set()
    for wf in words_f:
        all_words.update(get_words(wf))

    with open(my_words_f, 'w') as f:
        f.write('\n'.join(sorted(my_words - all_words)))


if __name__ == '__main__':
    main()
