#!/usr/bin/env python

import sys
import operator
import csv
import itertools
import datetime

def get_transaction_list(year):

    transactions = []
    header = []
    with open('dataset/NYPD_complete.csv') as f:
        csvline = csv.reader(f, delimiter=',')
        next(csvline) #skip header

        for line in csvline:
            line = [x.strip() for x in line]

            d,m,y = line[0].split("/")
            if int(y) == int(year):

                # append 's' to distingush susp from vic
                line[4] = 's' + line[4]
                line[5] = 's' + line[5]
                line[6] = 's' + line[6]
                line[7] = 'v' + line[7]
                line[8] = 'v' + line[8]
                line[9] = 'v' + line[9]

                transactions.append(line[2:9])

    return transactions

def get_item_list():

    item_list = []
    for line in transactions:
        for item in line:
            if item not in item_list:
                item_list.append(item)

    item_list.sort()
    return item_list

def get_support(cand_list, transactions):

    support = 0
    for line in transactions:
        items_to_check = [item in line for item in cand_list] # boolean check list

        if not (False in items_to_check):
            support += 1

    return support

def get_m_comb_list(oneitem_list, m=2):

    oneitem_list = [x[0] for x in oneitem_list]
    m_item_list = [list(x) for x in itertools.combinations(oneitem_list,m)] #return a combinations of m items list

    return m_item_list


def get_next_candidate_list(freq_itemsets_k):

    cand_list = []

    if not freq_itemsets_k:
        return cand_list

    num_freq = len(freq_itemsets_k)
    k = len(freq_itemsets_k[0])

    if k == 1:
        cand_list = get_m_comb_list(freq_itemsets_k, 2)
    else:
        new_list = [[freq_itemsets_k[0][:-1], [[freq_itemsets_k[0][-1]]]]] # use 1st frequent itemset

        for item in freq_itemsets_k[1:]:
            if new_list[-1][0] == item[:-1]:
                new_list[-1][1].append([item[-1]]) # append to the k-th element list
            else:
                new_list.append([item[:-1], [[item[-1]]]])

        for potential in new_list:  # obtain the size of k + 1 cand list
            leading, oneitem_list = potential

            if len(oneitem_list) > 1:
                cand_list.extend([leading+item for item in get_m_comb_list(oneitem_list, 2)])

    return cand_list

def get_freq_itemsets(item_list, transactions):

    freq_item_list = []
    candidates = [[item] for item in item_list]

    while len(candidates) > 0:
        freq_itemsets_k = [] # to store the candidate, which suppport >= min_support

        for cand in candidates:
            candidate_support = get_support(cand, transactions)

            if candidate_support >= min_support:
                freq_itemsets_k.append(cand)
                freq_item_list.append((cand, candidate_support))

        candidates = get_next_candidate_list(freq_itemsets_k) # update candidates

    return freq_item_list

def get_confidence(freq_item_list):

    f_dict = {} # create dictionary for the freq itemsets

    for freq_itemset in freq_item_list:
        f_dict[tuple(freq_itemset[0])] = freq_itemset[1]

    conf_list = []

    #time = datetime.datetime.now()

    """
    get "pre_rule" and "post_rule" list under association rule
    """

    for freq_itemset, support in freq_item_list:

        size = len(freq_itemset)

        if size > 1:    # consider the size > 1
            association_list = []

            for pre_rule_size in reversed(range(1, size)): # loop pre_rule in descending order

                for pre_rule_tuple in itertools.combinations(freq_itemset, pre_rule_size): # loop over all pre_rule combinations of current size
                    pre_rule = list(pre_rule_tuple)

                    post_rule = [x for x in freq_itemset if x not in pre_rule] # exclude pre_rule to find post_rule
                    association_list.append((pre_rule, post_rule))

            support_I = f_dict[tuple(freq_itemset)] # supp(pre_rule -> post_rule) = supp(I) share the same support

            while association_list: # extract pre_rule and post_rule
                pre_rule, post_rule = association_list[0]

                confidence = support_I / f_dict[tuple(pre_rule)]

                if confidence >= min_confidence:
                    conf_list.append((pre_rule, post_rule, support_I, confidence))
                else:
                    if len(pre_rule) > 1: # skip if one element in pre_rule
                        for pre_rule_remove_size in reversed(range(1, len(pre_rule))): # loop pre_rule in descending order
                            for I1_remove_tuple in itertools.combinations(pre_rule, pre_rule_remove_size): # loop over all pre_rule combinations of current size
                                pre_rule_remove_item = list(I1_remove_tuple)
                                post_rule_remove_item = [x for x in freq_itemset if x not in pre_rule_remove_item] # to find out post_rule by excluding pre_rule elements from the frequent itemset

                                try:
                                    association_list.remove((pre_rule_remove_item, post_rule_remove_item))
                                except ValueError:
                                    pass

                del association_list[0]

    #totalTime = float("{:.2f}".format( (datetime.datetime.now() - time).total_seconds() * 1000))

    return conf_list

start_year = 2006
end_year = 2021

for year in range(start_year,end_year):

    transactions = []
    item_list = []
    freq_item_list = []
    conf_list = []

    time = datetime.datetime.now()
    transactions = get_transaction_list(year)
    min_support = 0.01 * len(transactions) #0.05 ok
    min_confidence = 0.6

    item_list = get_item_list()
    freq_item_list = get_freq_itemsets(item_list, transactions)
    conf_list = get_confidence(freq_item_list)

    totalTime = float("{:.2f}".format( (datetime.datetime.now() - time).total_seconds() * 1000))

    print(f'year{year} elapsed time={totalTime}ms')

    output_file = "result/result_" + str(year) + ".txt"
    with open(output_file, 'w') as f:
        f.write(f'year{year} elapsed time={totalTime}ms\n')
        f.write(f'\ntotal transactions = {len(transactions)}\nmin support = {min_support}\nmin confidence = {min_confidence}')
        f.write(f'total items = {len(item_list)}\nitem list = {item_list}\n\n')
        f.write('*******************\n')
        f.write('Frequent itemsets:\n')
        for element in freq_item_list:
            f.write(str(element) + '\n')
        f.write('*******************\n\n')
        f.write('Association Rules with support >= ' + str(min_support) + ' and confidence >= ' + str(min_confidence) + '\n')
        for pre_rule, post_rule, supp, confidence in conf_list:
            f.write(str(pre_rule) + ' -> ' + str(post_rule) + ', support = ' + str(supp) + ' confidence = ' + str(round(confidence, 3))+ '\n')
