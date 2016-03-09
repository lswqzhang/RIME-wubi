#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2016-03-05 14:18:10
# @Author  : Weizhong Tu (mail@tuweizhong.com)
# @Link    : http://www.tuweizhong.com
# @Version : 0.0.1
from __future__ import unicode_literals
from collections import defaultdict
import os


class Wubi98Dict(object):
    WORD_MAYUAN_DICT = defaultdict(list)
    WORDMAYUAN_WEIGHT = defaultdict(lambda: 0)
    MAYUAN_WEIGHT = defaultdict(lambda: 0)

    def generate_single_word_dict(self, fpath):
        WORD_MAYUAN_DICT = defaultdict(list)
        f = open(fpath)
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                word, mayuan, weight = line.split()

                self.WORDMAYUAN_WEIGHT[word+mayuan] = weight
                self.MAYUAN_WEIGHT[mayuan] = weight

                WORD_MAYUAN_DICT[word].append(mayuan)
            except:
                print('error line: ', line)

        f.close()

        for word, mayuans in WORD_MAYUAN_DICT.items():
            self.WORD_MAYUAN_DICT[word] = sorted(
                mayuans, key=lambda x: len(x), reverse=True)

    def get_full_manyuan(self, word):
        return self.WORD_MAYUAN_DICT[word][0]

    def generate_mayuan(self, fdir):
        if not fdir.endswith('/'):
            fdir += '/'

        fdir_ok = '{}_mayuan/'.format(fdir[:-1])
        if not os.path.exists(fdir_ok):
            os.mkdir(fdir_ok)

        MY_WORD_MAYUAN_DICT = {}

        fs = os.listdir(fdir)
        for fpath in fs:
            if fpath.startswith(('.', '~')):
                continue

            f = open(fdir+fpath)
            f2 = open(fdir_ok+fpath, 'w')

            for line in f:
                line = line.strip()
                line_length = len(line)
                if line_length <= 1 or line in self.WORD_MAYUAN_DICT:
                    continue

                elif line_length == 2:
                    mayuan = [
                        self.get_full_manyuan(line[0])[:2],
                        self.get_full_manyuan(line[1])[:2],
                    ]
                elif line_length == 3:
                    mayuan = [
                        self.get_full_manyuan(line[0])[0],
                        self.get_full_manyuan(line[1])[0],
                        self.get_full_manyuan(line[2])[:2],
                    ]
                elif line_length >= 4:
                    mayuan = [
                        self.get_full_manyuan(line[0])[0],
                        self.get_full_manyuan(line[1])[0],
                        self.get_full_manyuan(line[2])[0],
                        self.get_full_manyuan(line[-1])[0],
                    ]

                mayuan_string = ''.join(mayuan)
                line_ok ='{}\t{}\n'.format(line, mayuan_string)

                # add new word to dict
                MY_WORD_MAYUAN_DICT[line] = mayuan_string

                f2.write(line_ok)

            f2.close()

        mayuan_words_dict = defaultdict(set)

        for word, mayuans in self.WORD_MAYUAN_DICT.items():
            for mayuan in mayuans:
                mayuan_words_dict[mayuan].add(word)

        for word, mayuan in MY_WORD_MAYUAN_DICT.items():
            mayuan_words_dict[mayuan].add(word)

        with open('./full_result.txt', 'w') as f:
            for mayuan in sorted(mayuan_words_dict):
                for word in mayuan_words_dict[mayuan]:

                    weight = self.WORDMAYUAN_WEIGHT[word+mayuan]
                    if weight == 0 and len(mayuan) == 4:
                        weight = self.MAYUAN_WEIGHT[mayuan]

                    f.write('{}\t{}\t{}\n'.format(word, mayuan, weight))

    def write_into_squirrel(self, fpath):
        print('write into squirrel')

        with open('full_result.txt') as f:
            content = f.read()

        with open(fpath) as f:
            header = f.read().rsplit('...', 1)[0]

        with open(fpath, 'w') as f:
            f.write('{}...\n{}'.format(header, content))


def main():
    wubi = Wubi98Dict()
    wubi.generate_single_word_dict('./qq_wubi.txt')
    wubi.generate_mayuan('./my_words')
    # wubi.write_into_squirrel('/Users/tu/Library/Rime/wubi98.dict.yaml')


if __name__ == '__main__':
    main()
    print('Done!')
