import os
import sys
import numpy as np
import argparse

def getIC(group):
    dic = {}
    ans_dic = {}
    for main_key in group:
        total = 0
        ans_dic[main_key] = 0

        for i in range(ord('A'), ord('Z') + 1):
            dic[chr(i)] = 0

        for letter in group[main_key]:
            if letter in dic:
                dic[letter] += 1

        for key in dic.keys():
            ni = dic[key]
            total += ni * (ni - 1)

        ans = float(total) / (len(group[main_key]) * (len(group[main_key]) - 1))
        ans_dic[main_key] = ans
    #print(ans_dic)
    return ans_dic


def grouping(text):
    ans_list = []
    for n in range(2, 11):
        group = {}
        for i in range(0, n):
            group[i] = []
            #print(group)
        for idx in range(0, len(text)):
            group[idx % n].append(text[idx])
        ans_dic = getIC(group)
        ans_list.append(ans_dic)
    return ans_list


def chiSquare(text, key_length):
    expected_freq = {"A": 0.08497, "B": 0.01492, "C": 0.02202, "D": 0.04253, "E": 0.11162,
                     "F": 0.02228, "G": 0.02015, "H": 0.06094, "I": 0.07546, "J": 0.00153,
                     "K": 0.01292, "L": 0.04025, "M": 0.02406, "N": 0.06749, "O": 0.07507,
                     "P": 0.01929, "Q": 0.00095, "R": 0.07587, "S": 0.06327, "T": 0.09356,
                     "U": 0.02758, "V": 0.00978, "W": 0.02560, "X": 0.00150, "Y": 0.01994, "Z": 0.00077}
    group = {}
    dic = {}

    for i in range(0, key_length):
        group[i] = []
    for idx in range(0, len(text)):
        group[idx % (key_length)].append(text[idx])
    
    # start counting chi-square for each group
    # shift means plus n then mod 26
    ans_list = []
    for k in group:
        chi, shift_n = float('inf'), 0
        shift_string = ''
        obs = []
        # shift n
        for n in range(0, 26):
            temp_string = ''
            temp_chi = 0
            for i in range(ord('A'), ord('Z') + 1):
                dic[chr(i)] = 0 
            for letter in group[k]:
                if letter in dic:
                    temp_string += chr((((ord(letter) - n - 65) % 26) + 65))
                    dic[chr(((ord(letter) - n - 65) % 26) + 65)] += 1
            for key in dic.keys():
                temp_chi += ((dic[key] - expected_freq[key]*len(group[k]))**2) / (expected_freq[key]*len(group[k]))
            #print('Group' + str(k+1) + ' shift ' + str(n) + ' : ' + str(temp_chi))
            if temp_chi < chi:
                shift_n = n
                chi = temp_chi
                shift_string = temp_string
                #print(shift_n, chi, ans_string)
        ans_list.append([shift_n, shift_string])
    return ans_list
        


if __name__ == '__main__':
    '''
    f = open('./q1.txt', 'r')
    line = f.read().strip().replace(' ', '').split('\n')
    f.close()
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", '--output_filename', default = 'output.txt', type = str)
    opt = parser.parse_args()

    print('Please enter the encrypted message: ')
    text = sys.stdin.readline()
    text = text.upper().replace(' ', '').replace('\n', '')

    #for text in line:
    avg, comp_avg, ley_length = 0, 0, 0
    #print(text) 
    ans_list = grouping(text)
    for _dic in ans_list:
        comp_avg = sum(_dic.values()) / len(_dic)
        if comp_avg > avg:
            avg = comp_avg
            key_length = len(_dic)

    print('\n##### Informations of Decrypting #####')
    print('Key Length = ' + str(key_length))
    string_list = chiSquare(text, key_length)
    #print(string_list)
    keyword = ''
    ans_string = [''] * len(text)
    for i in range(0, key_length):
        count = 0
        keyword += chr(string_list[i][0] + 65)
        for letter in string_list[i][1]:
            ans_string[i + count*key_length] = letter
            count += 1
            
    print('Keyword: ' + keyword)
    print('Plaintext: ' + ''.join(ans_string))
    f = open(opt.output_filename, 'w')
    f.write(''.join(ans_string))
    f.close()

