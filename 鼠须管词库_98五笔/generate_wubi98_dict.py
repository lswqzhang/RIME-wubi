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
    WORD_CODES_DICT = defaultdict(list)
    # 下载自网上的字词频率
    WORD_WEIGHT = defaultdict(lambda: 0)
    # 一级简码II
    WORDS_SET = {'戈', '子', '又', '大', '月', '土', '王', '目', '水', '日',
                 '口', '田', '山', '已', '火', '之', '金', '白', '木', '禾',
                 '立', '女', '几', '幺', '言'}

    def get_frequent_words(self):
        with open('./word7000.txt') as f:
            for line in f:
                try:
                    word, weight = line.split()
                except:
                    print(line)

                if word not in self.WORD_WEIGHT:
                    self.WORD_WEIGHT[word] = 7000 - int(weight)

    def generate_single_word_dict(self, fpath):
        f = open(fpath)
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                word, code = line.split()
            except ValueError:
                print('error line: ', line)
                continue

            if len(word) == 1:
                self.WORD_CODES_DICT[word].append(code)
        f.close()

        for word in self.WORD_CODES_DICT:
            self.WORD_CODES_DICT[word].sort(
                key=lambda x: len(x), reverse=True)

    def get_full_code(self, word):
        return self.WORD_CODES_DICT[word][0]

    def generate_words_code(self, fdir):
        if not fdir.endswith('/'):
            fdir += '/'

        fdir_ok = '{}_code/'.format(fdir[:-1])
        if not os.path.exists(fdir_ok):
            os.mkdir(fdir_ok)

        CUSTOM_WORDS_CODE_DICT = {}

        fs = os.listdir(fdir)
        for fpath in fs:
            if not fpath.endswith('.txt') or fpath.startswith(('.', '~')):
                continue

            f = open(fdir + fpath)
            f2 = open(fdir_ok + fpath, 'w')

            for line in f:
                line = line.strip()
                words_len = len(line)
                if words_len <= 1 or line in self.WORD_CODES_DICT:
                    continue

                elif words_len == 2:
                    code = [
                        self.get_full_code(line[0])[:2],
                        self.get_full_code(line[1])[:2],
                    ]
                elif words_len == 3:
                    code = [
                        self.get_full_code(line[0])[0],
                        self.get_full_code(line[1])[0],
                        self.get_full_code(line[2])[:2],
                    ]
                elif words_len >= 4:
                    code = [
                        self.get_full_code(line[0])[0],
                        self.get_full_code(line[1])[0],
                        self.get_full_code(line[2])[0],
                        self.get_full_code(line[-1])[0],
                    ]

                code_string = ''.join(code)
                line_ok = '{}\t{}\n'.format(line, code_string)

                # add new word to dict
                CUSTOM_WORDS_CODE_DICT[line] = code_string

                f2.write(line_ok)

            f2.close()

        code_words_dict = defaultdict(set)

        for word, codes in self.WORD_CODES_DICT.items():
            for code in codes:
                code_words_dict[code].add(word)

        for word, code in CUSTOM_WORDS_CODE_DICT.items():
            code_words_dict[code].add(word)

        with open('./full_result.txt', 'w') as f:
            for code in sorted(code_words_dict):
                for word in code_words_dict[code]:
                    weight = self.WORD_WEIGHT[word]

                    # 词语默认权重10，这样可以让词语在生辟字前
                    if weight == 0 and len(word) >= 2:
                        weight = 10

                    if len(word) == 1:
                        most_simple_code = self.WORD_CODES_DICT[word][-1]

                        # 一个汉字有简码的简码在前，但这个汉字的全码权重设置低一些
                        # 比如 “去” fc 但打 fcu 的时候第一个不显示“去”
                        if (code != most_simple_code and
                                len(self.WORD_CODES_DICT[word]) >= 2):
                            weight = 0

                            # 如果是常见的 7000 个字，全码也在繁体字前
                            if word in self.WORD_WEIGHT:
                                weight = 1

                    if len(code) == 1:
                        if word in self.WORDS_SET:
                            weight = 0
                        elif weight == 0:  # 一级简码如果词频中没有设置为6000
                            weight == 6000

                        stem = self.get_full_code(word)[:2]
                        print('word:', word, 'stem:', stem)
                        f.write('{}\t{}\t{}\t{}\n'.format(
                            word, code, weight, stem))
                    else:
                        f.write('{}\t{}\t{}\n'.format(word, code, weight))

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
    wubi.get_frequent_words()
    wubi.generate_single_word_dict('./wubi98_word_code.txt')
    wubi.generate_words_code('./my_words')
    wubi.write_into_squirrel('./RIME/wubi98.dict.yaml')

    # if os.path.exists('/Users/tu/Library/Rime/'):
    #     os.system('cp ./RIME/wubi98.dict.yaml /Users/tu/Library/Rime/')


if __name__ == '__main__':
    import sys
    if sys.version_info.major == 2:
        raise RuntimeError('please use Python 3')

    main()
    print('Done!')
