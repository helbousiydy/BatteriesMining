#!/usr/bin/env python
# -*- coding: utf-8 -*-

# __all__ = ['Capitalize_Liste', 'Remove_Duplicat', 'Clean_text', 'Experimental', 'copy_paste_text1', 'getyear',
#            'get_distance', 'Get_Sentences_And_After_Containing_Word', 'Get_Sentences_Containing_Word',
#            'Check_Keywords_CSV', 'Check_Current_Density', 'Check_the_unites_in_sentence_ONE', 'Check_end_Is_number',
#            'Check_ratio', 'Check_Number_Unit', 'Check_weight_ratio', 'is_number', 'Capitalize',
#            'Filtring_And_Checking_Keywords', 'Loading_range', 'Words_Before_and_after', 'Save_results_range',
#            'Save_results', 'Converting_From_PDF_OR_XML_To_TXT']


import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import itertools as it
import re
import string
import itertools
from KeyWordsExtractions.Current_Density import get_Crate, indices_Crate
from KeyWordsExtractions.Filtring_Functions import Filtring_Function
from KeyWordsExtractions.Converting_PDF_Or_XML_To_TXT import Converting_Function
import os
import numpy as np
import xlsxwriter
__all__ = ['Converting_From_PDF_OR_XML_To_TXT', 'Filtring_And_Checking_Keywords']
stop_words = set(stopwords.words('english'))


def Capitalize_Liste(liste):
    """
    :param liste: list of string
    :return: the same input list of string in lowercase, in capital letters and earache tring written letter by letter separately
    """

    new_liste = []
    new_liste1 = []
    first = liste[0]
    listes = [item.replace(' ', '-') for item in liste]
    liste = liste + listes
    listes = [item.replace('-', '−') for item in liste if '-' in item]
    liste = liste + listes
    for item in liste:
        new_liste.append(item.capitalize())
        new_liste.append(item.upper())
        new_liste.append(item.title())
    for item in new_liste:
        word = ' '.join(i for i in item)
        new_liste1.append(word)
    liste = liste + new_liste + new_liste1
    liste.insert(0, first)
    liste = Remove_Duplicat(liste)
    return liste


def Remove_Duplicat(seq):
    """
    :param seq: list
    :return: the same entry list removing duplicate elements
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


##################### Experemental Part Keywords #######################


########################################################################


def Clean_text(file):
    """
    :param file: the path to a text file
    :return: clean text
    """
    text = ''
    with open(file, 'r', encoding='utf8') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            try:
                if lines[i][-1] == '\n' and (lines[i][-2] == '-' or lines[i][-2] == '_'):
                    text_add = lines[i].replace('-\n', '').replace('_\n', '')
                    text = ''.join((text, text_add))
                else:
                    text = ''.join((text, lines[i]))
            except:
                pass
    stop = [item for item in string.punctuation if (item != ':' and item != '/' and item != '.' and item != '-' and item != ',')]
    stop.remove('%')
    liste = ['', '', '', '', '', '', '', '', '', '', '', '', '', '�']
    stop = stop + liste
    text.translate(str.maketrans('', '', str(stop)))
    text = re.sub("\s\s+", " ", text)
    text = text.replace('-', '−').replace('∼', '-')
    text = text.replace(' ac.', '~').replace(' a.c.', '~').replace(' a.c', '~').replace('(ac.', '~').replace('(a.c.','~').replace(
        '(a.c', '~').replace('\nac.', '~').replace('\na.c.', '~').replace('\na.c', '~')
    valid_characters = string.printable
    text = ''.join(i for i in text if i in valid_characters)
    return text


def Experimental(text):
    """
    :return: Experimental part
    """
    Exp = ['materials & methods', 'materials and methods', 'experimental details', 'experimental',
           'experimental section',
           'experimental part', 'computational and experimental methods', 'experimental methods', 'experimental method',
           'methods',
           'experimental and theoretical methods', 'Experimentals', 'Experimental and Computational Details',
           'experimental and computational details',
           'experimental setup', 'experimental assessment', 'methodology', 'experimental and computational detail',
           'experiment']
    Results = ['Result', 'Results', 'Discussion', 'Discussions', 'Results and discussion', 'Result and discussion',
               'Results and discussions', 'Result and discussions', 'Results and discussion']
    Ref = ['Reference', 'References', 'Conclusion', 'acknowledgement', 'In summary', 'In conclusion']
    Exp = Capitalize_Liste(Exp)
    Results = Capitalize_Liste(Results)
    Ref = Capitalize_Liste(Ref)
    experimental = []
    for exp in Exp:
        if exp in text:
            if text.split(exp, 1)[1].startswith('\n'):
                experimental.append(text.split(exp, 1)[1])

    if experimental != []:
        experimental = max(experimental, key=len)
        exp_result = []
        for result in Results:
            if result in experimental:
                if experimental.split(result, 1)[1].startswith('\n'):
                    exp_result.append(experimental.split(result)[0])
        if exp_result != []:
            exp_result = max(exp_result, key=len)
            experimental = exp_result
        else:
            references = []
            for ref in Ref:
                if ref in experimental:
                    if experimental.split(ref, 1)[1].startswith('\n'):
                        references.append(experimental.split(ref)[0])
            if references != []:
                references = max(references, key=len)
                experimental = references
    else:
        experimental = text
    experimental = experimental.replace('-', '−')
    return experimental


def copy_paste_text1(file, path):
    """
    :param file: path to text file
    :param path: the path where to paste the file
    """
    name = file.split('/')[-1][:-4]
    path = path + '/' + name + '.txt'
    f = open(file, 'r', encoding='utf8')
    try:
        with open(path, 'a', encoding='utf8') as f1:
            for x in f.readlines():
                f1.write(x)
            f.close()
            f1.close()
    except:
        try:
            path = '//?/' + path
            with open(path, 'a', encoding='utf8') as f1:
                for x in f.readlines():
                    f1.write(x)
                f.close()
                f1.close()
        except:
            print('There is an error during Copy_past!!!')
            pass


def getyear(text):
    """
    :return: year of publication of the article
    """
    for x in ['\n', ':', '>', '<', '/', '(', ')', '~', '[', ']', ',', ';', '(', ')', '@', '-', '_', '&', '*', '+', '©']:
        if x in text:
            text = text.replace(x, ' ')
    words = [x for x in text.split(' ') if len(x) > 0]
    minyear = 1990
    maxyear = 2019
    text_frac = 0.33
    years = []
    for i in range(0, int(len(words) * text_frac)):
        if words[i].isdigit() and len(words[i]) == 4:
            try:
                if int(words[i]) >= minyear and int(words[i]) <= maxyear:
                    years.append(int(words[i]))
            except ValueError:
                pass
    if len(years) == 0:
        for i in range(0, int(len(words))):
            if words[i].isdigit() and len(words[i]) == 4:
                try:
                    if int(words[i]) >= minyear and int(words[i]) <= maxyear:
                        years.append(int(words[i]))
                except ValueError:
                    pass
        if len(years) == 0:
            return 0
    result = max(years, key=years.count)
    return result


def get_distance(w1, w2, words):
    """
    :param w1: the first word
    :param w2: the second word
    :param words: list of strings
    :return: the distance of two strings in list
    """
    if w1 in words and w2 in words:
        w1_indexes = [index for index, value in enumerate(words) if value == w1]
        w2_indexes = [index for index, value in enumerate(words) if value == w2]
        distances = [abs(item[0] - item[1]) for item in itertools.product(w1_indexes, w2_indexes)]
        return min(distances)


def Get_Sentences_Containing_Word(text, word):
    """
    :return: the sentence that contains the word in the text
    """
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    document = text.split("\n\n")
    sent = []
    for paragraph in document:
        paragraph_sentence_list = tokenizer.tokenize(paragraph)
        for line in range(0, len(paragraph_sentence_list)):
            if word in paragraph_sentence_list[line]:
                sent.append(paragraph_sentence_list[line])
    sent = [item.replace('\n', ' ') for item in sent]
    return sent


def Get_Sentences_And_After_Containing_Word(text, word):
    """
    :return: the sentence that contains the word and the next sentence in the text
    """
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    document = text.split("\n\n")
    sent = []
    for paragraph in document:
        paragraph_sentence_list = tokenizer.tokenize(paragraph)
        for line in range(0, len(paragraph_sentence_list)):
            if word in paragraph_sentence_list[line]:
                try:
                    sent.append(paragraph_sentence_list[line] + paragraph_sentence_list[line + 1])
                except:
                    try:
                        sent.append(paragraph_sentence_list[line])
                    except:
                        try:
                            sent.append(paragraph_sentence_list[line] + paragraph_sentence_list[line + 1])
                        except:
                            sent.append(paragraph_sentence_list[line])
    return sent


def Check_weight_ratio(sent):
    """
    :param sent: the sentence of interest
    :return: wight ratios reported in the sentence if there is any in the format of : X:Y:Z or X/Y/Z
    """
    liste = []
    if sent.count(':') >= 1:
        stuff = re.findall(r"[-+]?\d*\.\d+|\d+", sent)
        stuff = [item for item in stuff if float(item) < 100]
        for L in range(0, 4):
            for subset in itertools.combinations(stuff, L):
                if (len(subset) == 3 or len(subset) == 2) and subset not in liste:
                    liste.append(subset)
        ratios = []
        if len(liste) != 0:
            liste = set(liste)
            for item in liste:
                ratio = ':'.join(item1 for item1 in item)
                ratios.append(ratio)
                ratio = ' :'.join(item1 for item1 in item)
                ratios.append(ratio)
                ratio = ': '.join(item1 for item1 in item)
                ratios.append(ratio)
                ratio = ' : '.join(item1 for item1 in item)
                ratios.append(ratio)
                ratio = '/'.join(item1 for item1 in item)
                ratios.append(ratio)
                ratio = ' /'.join(item1 for item1 in item)
                ratios.append(ratio)
                ratio = '/ '.join(item1 for item1 in item)
                ratios.append(ratio)
                ratio = ' / '.join(item1 for item1 in item)
                ratios.append(ratio)
        if ratios != []:
            ratios = set(ratios)
    else:
        ratios = []
    return ratios


def Check_Number_Unit(sent, units):
    """
    :param sent: the sentence of interest
    :param units: list of units of interest
    :return: if a unit is attached to the number or not and the the exact unit from the list of units
    """
    yes = False
    unit_yes = None
    for unit in units:
        if unit in sent:
            sent_before = sent.split(unit)[0]
            try:
                if sent_before[-1].isdigit():
                    yes = True
                    unit_yes = unit
            except:
                pass
    return yes, unit_yes


def Check_ratio(sent):
    """
    :param sent: the sentence of interest
    :return: ratios reported in the sentence if there is any
    """
    yes = False
    symboles = ['-', '−', '_', 'e', '≈', '~', 'ca.', 'c.a.', 'c.a', 'and', 'And', 'AND']
    ratio = re.findall(r"[-+]?\d*\.\d+|\d+", sent)
    ratio = [item for item in ratio if
             (((float(item) < 1) and (float(item) > 0)) or ((float(item) > -1) and (float(item) < 0)))]
    if ratio != []:
        for sym in symboles:
            sent = sent.replace(sym, '')
        words = sent.split(' ')
        for rat in ratio:
            if any(item.startswith(rat) for item in words):
                yes = True
    return yes, ratio


def is_number(s):
    """
    :return: if the string is a number on not
    """
    if s.replace('.', '', 1).isdigit():
        return True
    else:
        return False


def Capitalize(liste):
    """
    :param liste: list of string
    :return: the same input list of string in lowercase and in capital letters
    """
    new_liste = []
    liste = liste + [item.replace('-', '−') for item in liste]
    for item in liste:
        new_liste.append(item.capitalize())
        new_liste.append(item.upper())
        new_liste.append(item.title())
    liste = liste + new_liste
    liste = list(set(liste))
    return liste


def Check_end_Is_number(word):
    """
    :return: if the end of string is a number on not
    """
    num = re.findall(r"[-+]?\d*\.\d+|\d+", word)
    if len(num) == 1:
        return is_number(num[0])
    else:
        return False


def Loading_range(sent, unites, ratio):
    """
    :param sent: the sentence of interest
    :param unites: list of units
    :param ratio: list of ratios
    :return: if the value is reported as a range or exact value
    """
    unites_yes = []
    symboles = ['-', '−', '_', 'e', '≈', '~', '∼', 'ca.', 'c.a.', 'c.a', '–']
    and_ = ['≈', '~', '∼', '�', 'ca.']
    symboles_ = ['≈', '~', 'ca.', 'c.a.', 'c.a', '∼']
    range_words = ['typical', 'Typical', 'about', 'around', 'between', 'variable', ' range', 'ranging', 'varied',
                   'varies', 'average', 'approxima', 'more than', 'less than']
    exception = ['±', '+-', '-+', '�-', '�+', '-�', '+�', '� -', '� +', '- �', '+ �', '��']
    standard = ['standard deviation', 'STANDARD DEVIATION', 'confidence interval', 'CONFIDENCE INTERVAL', 'interval of confidence', 'INTERVAL OF CONFIDENCE',
                'standard-deviation', 'STANDARD-EVIATION', 'confidence-interval', 'CONFIDENCE-INTERVAL',
                'standard -deviation', 'STANDARD -EVIATION', 'confidence -interval', 'CONFIDENCE -INTERVAL',
                'standard- deviation', 'STANDARD- EVIATION', 'confidence- interval', 'CONFIDENCE- INTERVAL',
                'standard - deviation', 'STANDARD - EVIATION', 'confidence - interval', 'CONFIDENCE - INTERVAL']
    standard = standard + [item.replace('-', '−') for item in standard]
    standard = standard + [item.replace('-', '∼') for item in standard]
    range_words = Capitalize(range_words)
    range = False
    Done = False
    if ratio == []:
        for unit in unites:
            if unit in sent:
                unites_yes.append(unit)
        try:
            unit = max(unites_yes, key=len)
            sentence = sent.split(unit)[0]
            words = sentence.split()
            if len(words) >= 7:
                check = words[-7:]
                check = ' '.join(item for item in check)
            else:
                check = words
                check = ' '.join(item for item in check)
            if any(item in check for item in exception):
                Done = True
            if Done != True:
                words = words[::-1]
                if is_number(words[0]):
                    if any(item in words[1] for item in symboles):
                        if len(words[1]) == 1:
                            if Check_end_Is_number(words[2]):
                                range = True
                        elif any(words[1] == item for item in and_):
                            range = True
                        else:
                            word = ''.join(c for c in words[1] if c not in symboles)
                            if Check_end_Is_number(word):
                                range = True
                else:
                    for sym in symboles:
                        if sym in words[0]:
                            word = words[0].split(sym)
                            word = [item for item in word if item != '']
                            if len(word) == 1:
                                if (is_number(word[0]) and (sym in symboles_)) or (
                                        is_number(word[0]) and Check_end_Is_number(words[1])):
                                    range = True
                            elif len(word) == 2:
                                if (is_number(word[0]) and is_number(word[1])) or (
                                        is_number(word[1]) and Check_end_Is_number(word[0])):
                                    range = True
                            else:
                                try:
                                    if all(isinstance(float(x), (float, int)) for x in word):
                                        range = True
                                except:
                                    pass
                    if range != True and Done != True:
                        for sym in and_:
                            if words[0].startswith(sym):
                                range = True

        except:
            pass
        if range == False and Done != True:
            try:
                unit = max(unites_yes, key=len)
                sentence = sent.split(unit)[0]
                if any(item in sentence for item in range_words):
                    range = True
                else:
                    sentence = sent.split(unit)[1]
                    if any(item in sentence for item in standard):
                        range = True
            except:
                pass

    else:
        if Done != True:
            i = 0
            while i < (len(ratio) - 1):
                result = re.search(ratio[i] + '(.*)' + ratio[i + 1], sent)
                try:
                    sym = result.group(1)
                    syms = sym.split(' ')
                    for sym in syms:
                        if sym in symboles:
                            range = True
                except:
                    pass
                i += 1
            if range == False:
                sentence = sent.split(ratio[-1])[0]
                if any(item in sentence for item in range_words):
                    range = True
                else:
                    for rat in ratio:
                        try:
                            r = re.compile(r'\b%s\b' % rat, re.I)
                            m = r.search(sent)
                            i = m.start()
                            part = sent[i - 5:][:5]
                            if any(item in part for item in symboles):
                                range = True
                        except:
                            pass
    return range


def Check_the_unites_in_sentence_ONE(text, keyword):
    """
    :param keyword: the keyword of interest
    :return: - if the keyword is reported in the text or not, if so, it returns the sentence where the keyword is reported
             - if the keyword is reported as an exact value or as a range, if so, it returns the sentence where the keyword is reported
    """
    yes = False
    sentences_yes = []
    range_loading = False
    ratio = []
    sent_range = []
    if 'Electrode composition' in keyword:
        electrode = ['electrode', 'slurr', ' composit', 'cathode', 'anode']
        electrode = Capitalize_Liste(electrode)
        verbs = ['prepar', ' compos', 'mix', 'obtain', 'premix', 'consist', 'compris', 'contain', 'made', 'make',
                 'coat', 'cast', ' form', 'fabricat']
        wt = ['wt%', 'weight percentage', 'weight%', 'weight percentages', 'mass ratio',
              'weight ratio', 'weight ratios', 'weight-ratio', 'ratios weight', 'ratio weight',
              'weight fractions', 'weight fraction', 'weight %', 'wt %', 'weight.%', 'wt.%', 'wt.%', 'wt%',
              ' wt:',
              'weight %', 'wt %', 'weight.%', 'wt.%', 'wt.%', 'wt%', ' wt', ' wt:', 'wt ratio', '%']
        wt = Capitalize_Liste(wt)
        wt = Capitalize_Liste(wt)
        Not_to = ['performance', 'retention', 'efficiency']
        Not_to = Capitalize_Liste(Not_to)
        sentences = []
        for elec in electrode:
            sentences = sentences + Get_Sentences_Containing_Word(text, elec)
        if sentences != []:
            for sent in sentences:
                if len(sent.split()) <= 40:
                    electrode_ = ['electrode', 'slurr', 'cathode', 'anode']
                    if ' composit' in sent and not any(item in sent for item in electrode_):
                        verbs = ['prepar', 'mix', 'obtain', 'premix', 'consist', 'compris', 'contain', 'made', 'make',
                                 'coat', 'cast', ' form', 'fabricat']
                        verb = Capitalize_Liste(verbs)
                    else:
                        verb = Capitalize_Liste(verbs)
                    if any(item in sent for item in verb) and any(item in sent for item in wt):
                        stuff = re.findall(r"[-+]?\d*\.\d+|\d+", sent)
                        stuff = [item for item in stuff if float(item) < 100]
                        if len(stuff) >= 2:
                            yes = True
                    if yes != True:
                        liste = Check_weight_ratio(sent)
                        if any(item in sent for item in verb) and any(item in sent for item in liste):
                            yes = True
                else:
                    electrode_ = ['electrode', 'slurr', 'cathode', 'anode']
                    if ' composit' in sent and not any(item in sent for item in electrode_):
                        verbs = ['prepar', 'mix', 'obtain', 'premix', 'consist', 'compris', 'contain', 'made', 'make',
                                 'coat', 'cast', ' form', 'fabricat']
                        verb = Capitalize_Liste(verbs)
                    else:
                        verb = Capitalize_Liste(verbs)
                    if any(item in sent for item in verb) and any(item in sent for item in wt) and not any(
                            item in sent for item in Not_to):
                        yes = True
                    if yes != True:
                        liste = Check_weight_ratio(sent)
                        if any(item in sent for item in verb) and any(item in sent for item in liste) and not any(item in sent for item in Not_to):
                            yes = True

    elif 'Electrolyte composition' in keyword:
        electrolyte = ['electrolyte', 'soak', 'solution', 'wet', 'impregnate', ':EC', '/EC', '-EC', '(EC',
                       ' EC ', 'EC :', '-EC', ':EC', ' / EC', ' EC -', 'EC:', ' EC/', '+EC', 'ethylene carbonate',
                       'ethylene - carbonate', 'ethylenecarbonate', '(CH2O)2CO', 'C3H4O3', 'ethylene-carbonate',
                       'ethylene- carbonate', 'ethylene -carbonate', ' DMC ', '(DMC)', '-DMC', ':DMC', ' / DMC',
                       ' DMC -', ' DMC:', ' DMC/', 'dimethyl carbonate', ':DMC', ' / DMC', '-DMC', '(DMC', '+DMC',
                       'dimethyl - carbonate', 'dimethylcarbonate', '(CH3O)CO', 'OC(OCH3)2', 'C3H6O3',
                       'dimethyl-carbonate', 'dimethyl- carbonate', 'dimethyl -carbonate', '+PC',
                       ' PC :', 'PC-', ' PC:', ' PC/', ':PC', '/PC', '-PC', '(PC', 'propylene carbonate',
                       'propylene-carbonate', 'propylenecarbonate', 'CH3C2H3O2CO', 'C4H6O3', ' DEC ',
                       ' DEC-', ' DEC:', ' DEC/', ':DEC', '/DEC', '-DEC', '(DEC', 'diethyl carbonate',
                       'diethyl-carbonate', 'diethylcarbonate', 'OC(OCH2CH3)2', 'C5H10O3', '+EMC',
                       ' EMC ', 'EMC-', ' EMC:', ' EMC/', ':EMC', '/EMC', '-EMC', '(EMC', 'ethyl methyl carbonate',
                       'methyl ethyl carbonate', 'ethyl-methyl carbonate', 'methyl-ethyl carbonate',
                       'ethylmethyl carbonate', 'LiPF6', 'NaPF6',
                       'ethylmethylcarbonate', 'C4H8O3', 'LiClO4', 'NaClO4', 'lithium perchlorate', 'sodium perchlorate',
                        'lithium-perchlorate', 'sodium-perchlorate', 'ionic liquid', 'LiTFSI']
        electrolyte = Capitalize_Liste(electrolyte)
        electro_names = ['LP30', 'LP40', 'LP100', 'NP30', 'NP40', 'NP100']
        m = [' m ', ' M ', ' M)', 'M)', ' molar', ' M\n', ' mol L-1 ', ' mol L-1 ', ' mol L-1\n', ' mol L-1\n',
             ' mol/L ', ' mol/L ', ' mol dm−3', ' moldm−3', ' mol dm−3\n', ' moldm−3\n',
             ' mol dm −3', ' moldm −3', ' mol dm −3\n', ' moldm −3\n',
             ' mol dm− 3', ' moldm− 3', ' mol dm− 3\n', ' moldm− 3\n',
             ' mol dm − 3', ' moldm − 3', ' mol dm − 3\n', ' moldm − 3\n',
             ' mol/L\n', ' mol/L\n', ' molL-1 ', ' molvL-1 ', ' mol·L-1\n', ' molL-1\n', ' mol·L-1 ', ' mol·L-1 ',
             ' mol·L-1\n', ' mol·L-1\n',
             ' mol l-1 ', ' mol l-1 ', ' mol l-1\n', ' mol l-1\n', ' mol/l ', ' mol/l ', ' mol/l\n', ' mol/l\n',
             ' mol·l-1 ', ' mol·l-1 ', ' moll-1\n',
             ' mol·l-1\n', ' mol·l-1 ', ' mol-l-1 ', ' mol-l-1\n', ' mol-l-1\n']
        m = m + [item.replace('-', '�') for item in m]
        m = m + [item.replace('-', '−') for item in m]
        m = list(set(m))
        m1 = ['m ', 'M', 'M)', 'M)', 'molar', 'M', 'M\n', 'M\n', 'mol L-1', 'mol L-1', 'mol L-1\n', 'mol L-1\n',
              'mol/L', 'mol/L', 'mol/L\n', 'mol/L\n', 'mol·L-1', 'molL-1', 'mol·L-1\n', 'molL-1\n', 'mol·L-1', 'mol·L-1',
              'mol·L-1\n', 'mol·L-1\n', 'mol dm−3', 'moldm−3', 'mol dm−3\n', 'moldm−3\n', 'mol l-1', 'mol l-1',
              'mol l-1\n', 'mol l-1\n', 'mol/l', 'mol/l', 'mol/l\n', 'mol/l\n', 'mol·l-1', 'mol·l-1', 'mol·l-1\n',
              'mol·l-1\n', 'mol-l-1', 'mol-l-1\n', 'mol-l-1\n', 'mol·L–1', 'mol dm −3', 'moldm −3', 'mol dm −3\n',
              'moldm −3\n', 'mol dm− 3', 'moldm− 3', 'mol dm− 3\n', 'moldm− 3\n', 'mol dm − 3', 'moldm − 3', 'mol dm − 3\n',
              'moldm − 3\n']
        m1 = m1 + [item.replace('-', '�') for item in m1]
        m1 = m1 + [item.replace('-', '−') for item in m1]
        m1 = m1 + [item.replace('-', '–') for item in m1]
        m1 = list(set(m1))
        sentences = []
        for elec in electrolyte:
            sent_1 = Get_Sentences_Containing_Word(text, elec)
            if sent_1 != []:
                remove = Capitalize_Liste([elec])
                electrolyte_others = [item for item in electrolyte if item not in remove]
                for sent in sent_1:
                    if any(item in sent for item in electrolyte_others):
                        sentences.append(sent)

        if sentences != []:
            sentences = list(set(sentences))
            for sent in sentences:
                if any(item in sent for item in m):
                    yes = True
                else:
                    if Check_Number_Unit(sent, m1)[0] == True:
                        yes = True
        if yes == False:
            for word in electro_names:
                if word in text:
                    yes = True

    elif 'Separator' in keyword:
        separators = ['film', 'membrane', 'sheet', 'Celgard', 'celgard', 'Whatman', 'whatman', 'propylene', 'ethylene',
                      'glass fiber']
        separators = Capitalize_Liste(separators)
        separat = ['separator', 'separate']
        separat = Capitalize_Liste(separat)
        sentences = []
        for elec in separat:
            sentences = sentences + Get_Sentences_Containing_Word(text, elec)
        if sentences != []:
            for sent in sentences:
                if any(item in sent for item in separators):
                    yes = True

    elif 'Electrode surface area' in keyword:
        electrode = ['disk', 'disc ', 'discs ', 'disc\n', 'discs\n', 'electrode', 'mixture',
                      'driedfilm', 'cathode', 'anode',
                     'dried - film',  'dried- film', 'dried -film', 'dried-film']
        electrode = Capitalize_Liste(electrode)
        electrode_2 = ['Ø','punch','diameter', 'ø', 'pouch', 'cut']
        electrode_2 = Capitalize_Liste(electrode_2)
        electrode_Not = ['reference', 'counter', 'lithium metal', 'Li metal', 'Li-metal', 'sodium metal', 'Na metal', 'Na-metal',
                         'steel', 'titanium', 'Ti ', 'Ti,', 'Ti.', 'electrodeposition',
                         'platinum', 'Platinum', 'Pt ', 'Pt,', 'Pt.']
        electrode_Not = Capitalize_Liste(electrode_Not)
        electrode_area = ['electrode surface area', 'surface area of the electrode',
                          'geometrical surface area of electrode',
                          'geometrical surface area of the electrode', 'surface area electrodes',
                          'geometric surface area', 'electrode area', 'electrodes area', 'cathode area',
                          'cathodes area',
                          'anode area', 'anodes area', 'cathode surface area',
                          'anode surface area', 'current collector']
        electrode_area = Capitalize_Liste(electrode_area)
        unites_area = ['mm 2', 'mm2', 'mm-2', 'mm -2', 'mm- 2', 'mm - 2', 'cm 2', 'cm2', 'cm-2', 'cm -2', 'cm- 2',
                       'cm - 2',
                       'mm �2', 'mmv2', 'mm� 2', 'mm�2', 'mm � 2', 'millimeter square', 'cm �2', 'cm�2', 'cm� 2',
                       'cm � 2',
                       'cmv2', 'centimeter square', 'dm 2', 'dm2', 'dm-2', 'dm -2', 'dm- 2', 'dm - 2',
                       'dm �2', 'dmv2', 'dm� 2', 'dm�2', 'dm � 2', 'decimeter square',
                       'in 2', 'in2', 'in-2', 'in -2', 'in- 2', 'in - 2',
                       'in �2', 'inv2', 'in� 2', 'in�2', 'in � 2', 'inches square', 'inch square',
                       'inch 2', 'inch2', 'inch-2', 'inch -2', 'inch- 2', 'inch - 2',
                       'inch �2', 'inchv2', 'inch� 2', 'inch�2', 'inch � 2',
                       'inches 2', 'inches2', 'inches-2', 'inches -2', 'inches- 2', 'inches - 2',
                       'inches �2', 'inchesv2', 'inches� 2', 'inches�2', 'inches � 2',
                       'lm 2', 'lm2', 'lm-2', 'lm -2', 'lm- 2', 'lm - 2',
                       'lm �2', 'lmv2', 'lm� 2', 'lm�2', 'lm � 2'
                       'µm 2', 'µm2', 'µm-2', 'µm -2', 'µm- 2', 'µm - 2',
                       'µm �2', 'µmv2', 'µm� 2', 'µm�2', 'µm � 2', 'micrometer square',
                       '�m 2', '�m2', '�m-2', '�m -2', '�m- 2', '�m - 2',
                       '�m �2', '�mv2', '�m� 2', '�m�2', '�m � 2']
        unites_area = unites_area + [item.replace('-', '−') for item in unites_area]
        unites_area = unites_area + [item.replace('-', '–') for item in unites_area]
        unites_area = list(set(unites_area))
        unites = [ ' in,', ' in;', ' in.', ' in)', ' in)',
                   ' mm ', ' cm ', ' μm', ' µm', ' dm ', ' mm,', ' cm,', ' dm,', ' mm.', ' cm.', ' dm.', ' mm)', ' cm)', ' dm)',
                   ' inch', ' μm', ' lm ', ' µm', ' nm-', ' mm-', ' mm', ' mm;', ' �m', ' mm ', ' mm,', ' mm)', ' micrometer', ' mm-', ' mm,',
                   ' mm ', ' μ m', ' l m ', ' decimeter']
        unites = unites + [item.replace('-', '−') for item in unites]
        unites = unites + [item.replace('-', '–') for item in unites]
        unites = list(set(unites))
        unites1 = ['in ', 'in ', 'in,', 'in;', 'in.', 'in)', ' in)',
                   'mm ', 'cm ', 'μm', 'µm', 'dm ', 'mm,', 'cm,', 'dm,', 'mm.', 'cm.', 'dm.', 'mm)', 'cm)', 'dm)',
                   'inch', 'μm', 'lm ', 'µm', 'nm-', 'mm-', 'mm', 'mm;', '�m', 'mm ', 'mm,', 'mm)', 'micrometer', 'mm-', 'mm,',
                   'mm ', 'μ m', 'l m ', 'decimeter']
        unites1 = unites1 + [item.replace('-', '−') for item in unites1]
        unites1 = unites1 + [item.replace('-', '–') for item in unites1]
        unites1 = list(set(unites1))
        sentences = []
        for elec in electrode_area:
            sentences = sentences + Get_Sentences_Containing_Word(text, elec)
        if sentences != []:
            sentences = list(set(sentences))
            for sent in sentences:
                if any(item in sent for item in unites_area):
                    yes = True
        sentences = []
        for elec in electrode:
            sentences = sentences + Get_Sentences_Containing_Word(text, elec)
        if sentences != []:
            sentences = list(set(sentences))
            for sent in sentences:
                if any(item in sent for item in unites) and any(item in sent for item in electrode_2) and not any(item in sent for item in electrode_Not):
                    yes = True
                else:
                    if Check_Number_Unit(sent, unites1)[0] == True and not any(item in sent for item in electrode_Not) and any(item in sent for item in electrode_2):
                        yes = True

    elif 'Electrode thickness' in keyword:
        electrode = ['electrode', ' composit', 'anode', 'cathode']
        electrode = Capitalize_Liste(electrode)
        thickness = ['thick', ' thin', 'Thick', ' Thin']
        thickness = Capitalize_Liste(thickness)
        unites = ['μm', 'µ m', ' nm-', ' mm-', ' mm', 'mm;', ' �m', ' nm', ' nm ', ' mm ', ' nm,', ' mm,', ' nm.',
                  ' mm.', ' nm)', ' lm', ' l m',
                  ' mm)', 'micrometer', 'mm-thick', 'mm-', 'mm,', 'mm ', 'μ m']
        unites = unites + [item.replace('-', '−') for item in unites]
        unites1 = ['µm', 'µ m', 'mm', '�m', 'micrometer', 'nm', 'lm', 'l m']
        unites1 = list(set(unites1))
        unites = list(set(unites))
        Not_Consider = ['slurr', 'cast', 'doctor blade', 'doctorblade', 'dr blad', 'dr. blad', 'dr.blad',
                        'reference', 'counter', 'lithium metal', 'lithium-metal', 'Li metal', 'Li-metal',
                        'lithium foil', 'Li foil', 'Celgard', 'Whatman',
                        'Li -metal', 'Li- metal', 'Li - metal', 'Li -foil', 'Li- foil', 'Li - foil',
                        'Li-foil', 'copper metal', 'Cu metal', 'Cu-metal', 'copper foil', 'Cu foil', 'Cu-foil',
                        'copper disc', 'Cu disc', 'Cu-disc', 'sodium metal', 'Na metal', 'Na-metal', 'sodium foil',
                        'Na foil', 'Na-foil', 'sodium disc', 'Na disc', 'Na-disc', 'steel foil', 'steel disc',
                        'separator',
                        'lithium disc', 'Li disc', 'Li-disc', ' coat', 'passivation layer', 'SEI', 'Doctor Blade',
                        'Doctor-Blade', ' cell ', ' cells ', 'current collector', 'precipit', 'deposit']

        Not_Consider = Capitalize_Liste(Not_Consider)
        sentences = []
        for elec in electrode:
            sentences = sentences + Get_Sentences_Containing_Word(text, elec)
        if sentences != []:
            sentences = list(set(sentences))
            for sent in sentences:
                if any(item in sent for item in thickness) and any(item in sent for item in unites) and not any(
                        item in sent for item in Not_Consider):
                    if not Loading_range(sent, unites, ratio):
                        yes = True
                        sentences_yes.append([keyword, sent])
                        sent_range.append([sent, 'Exact'])
                    else:
                        range_loading = True
                        yes = True
                        sentences_yes.append([keyword, sent])
                        sent_range.append([sent, 'Range'])
                    if Check_Number_Unit(sent, unites1) == True and any(item in sent for item in thickness) and not any(
                            item in sent for item in Not_Consider):
                        if not Loading_range(sent, unites, ratio):
                            yes = True
                            sentences_yes.append([keyword, sent])
                            sent_range.append([sent, 'Exact'])
                        else:
                            range_loading = True
                            yes = True
                            sentences_yes.append([keyword, sent])
                            sent_range.append([sent, 'Range'])

    elif 'Slurry casting method' in keyword:
        slurry = ['Slurry casting method', 'slurry casting', 'ball-milling procedure', 'doctorblade', 'dr.blad',
                  'ball milling procedure', 'solvent evaporation', 'film applicator', 'doctor blad', 'dr blad',
                  'dr. blad', 'tape cast', 'tape-cast', 'film coater', 'film-coater', 'cast', 'Doctor Blade',
                  'Doctor-Blade']
        slurry = Capitalize_Liste(slurry)
        sentences = []
        for slurr in slurry:
            sentences = sentences + Get_Sentences_Containing_Word(text, slurr)
        if sentences != []:
            sentences = list(set(sentences))
            yes = True
            for sent in sentences:
                sentences_yes.append([keyword, sent])

    elif 'Electrolyte volume' in keyword:
        electrolyte = ['Electrolyte volume', 'electrolyte volume', 'volume of electrolyte', 'volume of electrolytes',
                       'electrolytes volume']
        electrolyte = Capitalize_Liste(electrolyte)
        unites = ['µL', 'µl', 'µ L', 'µ l', 'µl cm−2', 'µl cm −2', 'µl cm− 2', 'µl cm − 2', 'µl cm2', 'µl cm 2', 'mL',
                  'ml', 'ml cm−2', 'ml cm −2', 'ml cm− 2', 'ml cm − 2', 'ml cm2', 'ml cm 2', '�L', '�l', '�l cm−2',
                  '�l cm    −2', '�l cm− 2', '�l cm − 2', '�l cm2', '�l cm 2',
                  ' lL', ' ll', ' l L', ' l l', ' ll cm−2', ' ll cm −2', ' ll cm− 2', ' ll cm − 2', ' ll cm2', ' ll cm 2']
        unites = unites + [item.replace('-', '−') for item in unites]
        unites = unites + [item.replace('-', '–') for item in unites]
        unites = list(set(unites))
        sentences = []
        for elec in electrolyte:
            sentences = sentences + Get_Sentences_Containing_Word(text, elec)
        if sentences != []:
            sentences = list(set(sentences))
            for sent in sentences:
                if any(item in sent for item in unites):
                    yes = True

        if yes != True:
            electrolyte = ['electrolyte', 'soak', 'solution', 'wet', 'impregnate', ':EC', '/EC', '-EC', '(EC',
                           ' EC ', 'EC :', '-EC', ':EC', ' / EC', ' EC -', 'EC:', ' EC/', '+EC', 'ethylene carbonate',
                           'ethylene - carbonate', 'ethylenecarbonate', '(CH2O)2CO', 'C3H4O3',
                           'ethylene-carbonate', 'ethylene- carbonate', 'ethylene -carbonate',
                           ' DMC ', '(DMC)', '-DMC', ':DMC', ' / DMC', ' DMC -', ' DMC:', ' DMC/', 'dimethyl carbonate',
                           ':DMC', ' / DMC', '-DMC', '(DMC', '+DMC',
                           'dimethyl - carbonate', 'dimethylcarbonate', '(CH3O)CO', 'OC(OCH3)2', 'C3H6O3',
                           'dimethyl-carbonate', 'dimethyl- carbonate', 'dimethyl -carbonate', '+PC',
                           ' PC :', 'PC-', ' PC:', ' PC/', ':PC', '/PC', '-PC', '(PC', 'propylene carbonate',
                           'propylene-carbonate', 'propylenecarbonate', 'CH3C2H3O2CO', 'C4H6O3', ' DEC ',
                           ' DEC-', ' DEC:', ' DEC/', ':DEC', '/DEC', '-DEC', '(DEC', 'diethyl carbonate',
                           'diethyl-carbonate', 'diethylcarbonate', 'OC(OCH2CH3)2', 'C5H10O3', '+EMC',
                           ' EMC ', 'EMC-', ' EMC:', ' EMC/', ':EMC', '/EMC', '-EMC', '(EMC', 'ethyl methyl carbonate',
                           'methyl ethyl carbonate', 'ethyl-methyl carbonate', 'methyl-ethyl carbonate',
                           'ethylmethyl carbonate', 'LiPF6', 'NaPF6', 'ethylmethylcarbonate', 'C4H8O3', 'LiClO4', 'NaClO4',
                           'lithium perchlorate', 'sodium perchlorate',  'lithium-perchlorate',
                           'sodium-perchlorate', 'ionic liquid', 'LiTFSI']
            electrolyte = Capitalize_Liste(electrolyte)
            electro_names = ['LP30', 'LP40', 'LP100', 'NP30', 'NP40', 'NP100']
            electrolyte = Capitalize_Liste(electrolyte)
            sentences = []
            for elec in electrolyte:
                sent_1 = Get_Sentences_Containing_Word(text, elec)
                if sent_1 != []:
                    remove = Capitalize_Liste([elec])
                    electrolyte_others = [item for item in electrolyte if item not in remove]
                    for sent in sent_1:
                        if any(item in sent for item in electrolyte_others):
                            sentences.append(sent)
            for elec in electro_names:
                sentences = sentences + Get_Sentences_Containing_Word(text, elec)
            if sentences != []:
                sentences = list(set(sentences))
                for sent in sentences:
                    if any(item in sent for item in unites):
                        yes = True

    elif 'Electrode porosity' in keyword:
        porosity = ['porosity', 'porosities', 'Porosity', 'Porosities']
        unites = ['%']
        Not_To_Consider = ['membrane', 'separator', 'polymer', 'Membrane', 'Separator', 'Polymer', 'Foam',
                           'electrolyte', 'lithiation', 'Bruggeman', 'Bruggman', 'expansion', 'foam',
                           'mesoporosity', 'meso porosity', 'meso-porosity',
                           'microporosity', 'micro porosity', 'micro-porosity',
                           'nanoporosity', 'nano porosity', 'nano-porosity', 'particle',
                           'macroporosity', 'macro porosity', 'macro-porosity', 'pore size distribution']
        Not_To_Consider = Capitalize(Not_To_Consider)
        sentences = []
        for elec in porosity:
            sentences = sentences + Get_Sentences_Containing_Word(text, elec)
        if sentences != []:
            sentences = list(set(sentences))
            for sent in sentences:
                if not any(item in sent for item in Not_To_Consider) and ((any(item in sent for item in unites) or Check_ratio(sent)[0])):
                    if len(Check_ratio(sent)[1]) >= 1:
                        ratio = Check_ratio(sent)[1]
                    if not Loading_range(sent, unites, ratio):
                        yes = True
                        sentences_yes.append([keyword, sent])
                        sent_range.append([sent, 'Exact'])
                    else:
                        range_loading = True
                        yes = True
                        sentences_yes.append([keyword, sent])
                        sent_range.append([sent, 'Range'])

    elif 'Mass loading' in keyword:
        loading = ['Standard deviation loading', 'standard deviation loading', 'load', 'areal density', 'area density',
                   'surface density', 'superficial density', 'areic density', 'mass thickness', 'column density',
                   'density thickness']
        unites = ['g /cm�\x002', 'mgcm\x002', 'g/ cm2', 'mg cm �\x002', 'gcm -\x002', 'g/cm2', 'mg cm\x002',
                  'mg cm −\x002', 'mg/ cm2', 'mg·cm2', 'gcm \x002',
                  'gcm �\x002', 'mgcm \x002', ' gcm2', 'g cm- \x002', 'g cm�\x002', 'g/ cm�2', 'mg / cm�2',
                  'g/ cm�\x002', 'g cm-\x002', 'mg cm -\x002',
                  'mg/cm�2', 'mg cm�2', 'g /cm�2', 'mg  cm−\x002', 'g / cm2', 'mgcm−\x002', 'mg cm \x002',
                  'mg cm-\x002', 'g/cm 2', 'g / cm�\x002', 'mg cm -2',
                  'mg/cm 2', 'mgcm2', 'g cm �2', 'mg/cm �2', 'mgcm �2', 'mgcm�\x002', ' gcm\x002', 'mg cm2', 'mg /cm2',
                  'mg cm −2', 'mg cm�\x002', 'mg cm 2',
                  'mgcm -2', 'mg cm� 2', 'mgcm�2', 'g/cm �2', 'mg cm−2', 'mgcm � \x002', 'mg cm−\x002', 'g cm 2',
                  'mgcm−2', 'mg cm- \x002', 'mgcm �',
                  'mg per cm2', 'mg per cm�2', 'g/cm �\x002', 'g/cm�2', 'g/ cm', 'gcm 2', 'mg cm �2', 'mg (cm2)−1',
                  ' gm²', 'g cm�2', 'mg (cm2)−\x001', 'g/cm\x002',
                  'g cm\x002', 'g / cm�2', 'g cm �\x002', 'mg/cm2', 'mg / cm2', 'g cm -2',
                  'mg of active material per cm�\x002', 'g/cm \x002', 'mg cm-2',
                  'mg of active material per cm2', 'mg/cm \x002', 'g /cm2', 'mg  cm−2', 'g cm- 2', 'g/m²', 'mgcm 2',
                  'gcm �2', 'mg per cm�\x002', 'mg·cm\x002',
                  'g cm \x002', 'gcm -2', 'mgcm -\x002', 'mg /cm�2', 'g cm -\x002', 'mg of active material per cm�2',
                  'mg cm–2', 'mg cm- 2', 'g cm2', 'g cm-2',
                  'mg/ cm�2', 'mg cm–\x002']
        unites = [item.replace('-', '−') for item in unites]
        unites = [item.replace('-', '–') for item in unites]
        loading = Capitalize_Liste(loading)
        sentences = []
        for elec in loading:
            sentences = sentences + Get_Sentences_And_After_Containing_Word(text, elec)
        if sentences != []:
            sentences = list(set(sentences))
            for sent in sentences:
                if any(item in sent for item in unites):
                    if not Loading_range(sent, unites, ratio):
                        yes = True
                        sentences_yes.append([keyword, sent])
                        sent_range.append([sent, 'Exact'])
                    else:
                        range_loading = True
                        yes = True
                        sentences_yes.append([keyword, sent])
                        sent_range.append([sent, 'Range'])

    elif 'Cutoff voltage' in keyword:
        voltage = ['voltage', 'potential']
        limit = ['cutoff', 'cut-off', 'cut−off', 'cut–off', 'cut -off', 'cut −off', 'cut –off',
                  'cut- off', 'cut− off', 'cut– off', 'cut - off', 'cut − off', 'cut – off',
                  'final', 'range', 'limit', 'window', 'domain', 'cell']
        unites = [' v ', ' mv ', ' v.', ' mv.', ' v,', ' mv,', ' v;', ' mv;',
                  ' v)', ' mv)', ' V)', ' MV)', ' mV)',
                  ' V ', ' MV ', ' V.', ' MV.', ' V,', ' MV,', ' V;', ' MV;',
                  ' mV ', ' mV.', ' mV,', ' mV;']
        unites_ = ['v ', 'mv ', 'v.', 'mv.', 'v,', 'mv,', 'v;', 'mv;',
                   'v)', 'mv)', 'V)', 'MV)', 'mV)',
                   'V ', 'MV ', 'V.', 'MV.', 'V,', 'MV,', 'V;', 'MV;',
                   'mV ', 'mV.', 'mV,', 'mV;']
        voltage = Capitalize_Liste(voltage)
        Extra = ['frequenc', 'scan rate', 'scanning rate', 'scanrate', 'scan-rate', 'scan -rate', 'scan- rate', 'scan - rate',
                 'scan−rate', 'scan −rate', 'scan− rate', 'scan − rate', 'scan–rate', 'scan –rate', 'scan– rate', 'scan – rate',
                 'impedance', 'voltammetr']
        Extra = Capitalize_Liste(Extra)
        sentences = []
        for elec in voltage:
            sentences = sentences + Get_Sentences_Containing_Word(text, elec)
        if sentences != []:
            sentences = list(set(sentences))
            for sent in sentences:
                if any(item in sent for item in unites) and any(item in sent for item in limit) and not any(item in sent for item in Extra):
                    yes = True
                elif Check_Number_Unit(sent, unites_) == True and any(item in sent for item in limit) and not any(item in sent for item in Extra):
                    yes = True
        if yes != True:
            cycled = ['cycl', 'charg', 'discharg', 'galvan']
            cycled = Capitalize_Liste(cycled)
            between = ['between', 'from', 'rang', 'curve', 'cell', 'batter', 'performanc']
            between = Capitalize_Liste(between)
            sentences = []
            for elec in cycled:
                sentences = sentences + Get_Sentences_Containing_Word(text, elec)
            if sentences != []:
                sentences = list(set(sentences))
                for sent in sentences:
                    if any(item in sent for item in unites) and any(item in sent for item in between) and not any(item in sent for item in Extra):
                        yes = True
                    elif Check_Number_Unit(sent, unites_) == True and any(item in sent for item in between) and not any(item in sent for item in Extra):
                        yes = True

    elif 'Current density' in keyword:
        yes, c_rate = Check_Current_Density(text)
        if yes == True:
            sentences_yes.append([keyword, c_rate])

    return yes, sentences_yes, range_loading, sent_range


def Words_Before_and_after(words, item, nbr):
    """
    :param words: list of words
    :param item: word of interest
    :param nbr: number of words wanted before and after the word of interest
    :return: list of words before and after the word of interest
    """
    liste = [[words[item], item]]
    for n in range(nbr):
        try:
            liste.append([words[item + n +1], item + n +1])
        except:
            pass
        try:
            liste.insert(0, [words[item - (n+1)], item - (n+1)])
        except:
            pass
    return liste


def Check_Current_Density(text):
    """
    :return: if the current density and c_rate are reported in the text or not
    """
    current_density = False
    text = text.replace('�', '')
    text = text.replace('−', '-')
    text = text.replace('-', '-')
    indices_Crate_C, indices_Crate_mg, indices_Crate_Akg, indices_Crate_Ag, c_rate_indices77, indices_Crate_cm = indices_Crate(text)
    C_rate = get_Crate(indices_Crate_C, indices_Crate_mg, indices_Crate_Akg, indices_Crate_Ag, c_rate_indices77,
                       indices_Crate_cm, text)
    C = ['rate', 'current densit', 'currentdensit', 'current-densit'
                  , 'current- densit', 'current -densit', 'current - densit', 'cycle', 'capacity']
    C_rate_yes = ''
    if C_rate != []:
        words = text.split()
        for c_rate in C_rate:
            sent = Words_Before_and_after(words, c_rate[1], 15)
            sent = ' '.join(item[0] for item in sent)
            if any(item in sent for item in C):
                current_density = True
                C_rate_yes = C_rate_yes + '\n' + ' --> ' + sent

    return current_density, C_rate_yes


def Check_Keywords_CSV(temp_path):
    """
    :param temp_path: path to TXTs files
    :return: - for each article, whether each keyword is reported or not
             - for some keywords, whether it is reported as exact value or as range
    """
    keywords = ['Electrode composition', 'Electrolyte composition', 'Separator', 'Electrode surface area',
                'Electrode thickness', 'Slurry casting method', 'Electrolyte volume',
                'Electrode porosity', 'Mass loading', 'Current density', 'Cutoff voltage']
    path = temp_path
    files_short = np.array([f for f in os.listdir(temp_path) if os.path.isfile(os.path.join(temp_path, f))])
    files = np.array([temp_path + '/' + f for f in files_short])
    ############################################################################
    Cycling_conditions = ['Current density', 'C-rate', 'Resting time', 'Open circuit voltage time']
    keywords_range = ['Electrode thickness', 'Electrode porosity', 'Mass loading']
    a = 1
    r = 1
    all_results = []
    range_Yes_No = [[], [], []]
    if keywords[0] == 'Electrode composition':
        keyword = keywords[0]
        for file in files:
            print(file)
            print('Article ', a, ': First filter with "Electrode composition"')
            text_all = Clean_text(file)
            text_exp = Experimental(text_all)
            text = text_exp
            stop = ['(', ')', '[', ']', '"', '@', '~', '*', '+', '\\']
            text = ''.join(item for item in text if not item in stop)
            year = getyear(open(file, 'r', encoding='utf8').read())
            results = 'Article ' + str(a) + ',' + str(year)
            yes = 'No'
            value_yes, sentences_yes, range_loading, sent_range = Check_the_unites_in_sentence_ONE(text, keyword)
            if value_yes == True:
                yes = 'Yes'
            if yes == 'Yes':
                if range_loading == False:
                    path_yes = path + '/' + str(keyword) + '/' + keyword + '_Yes'
                    if not os.path.exists(path_yes):
                        os.makedirs(path_yes)
                    copy_paste_text1(file, path_yes)
                elif range_loading == True:
                    path_yes = path + '/' + str(keyword) + '/' + keyword + '_With_Range'
                    if not os.path.exists(path_yes):
                        os.makedirs(path_yes)
                    copy_paste_text1(file, path_yes)
            else:
                path_yes = path + '/' + str(keyword) + '/' + keyword + '_No'
                if not os.path.exists(path_yes):
                    os.makedirs(path_yes)
                copy_paste_text1(file, path_yes)
            a += 1
        print('"Electrode composition" filter is finished')
        if keywords != []:
            temp_path = path + '/' + str(keyword) + '/' + keyword + '_Yes'
            if not os.path.exists(temp_path):
                os.makedirs(temp_path)
            files_short = np.array([f for f in os.listdir(temp_path) if os.path.isfile(os.path.join(temp_path, f))])
            files = np.array([temp_path + '/' + f for f in files_short])
            a = 1
            for file in files:
                Range = False
                print(file)
                print('Article ', a, ': ')
                text_all = Clean_text(file)
                text_exp = Experimental(text_all)
                text = text_exp
                stop = ['(', ')', '[', ']', '"', '@', '~', '*', '+', '\\']
                text = ''.join(item for item in text if not item in stop)
                year = getyear(open(file, 'r', encoding='utf8').read())
                results = 'Article ' + str(a) + ',' + str(year)
                for keyword in keywords:
                    yes = 'No'
                    if keyword in Cycling_conditions:
                        text = text_all
                    value_yes, sentences_yes, range_loading, sent_range = Check_the_unites_in_sentence_ONE(text, keyword)
                    if value_yes == True:
                        yes = 'Yes'
                    if yes == 'Yes':
                        results = ','.join((results, yes))
                        results = ','.join((results, str(range_loading)))
                        if range_loading == False:
                            path_yes = path + '/' + str(keyword) + '/' + keyword + '_Yes'
                            if not os.path.exists(path_yes):
                                os.makedirs(path_yes)
                            copy_paste_text1(file, path_yes)
                        elif range_loading == True:
                            path_yes = path + '/' + str(keyword) + '/' + keyword + '_With_Range'
                            if not os.path.exists(path_yes):
                                os.makedirs(path_yes)
                            copy_paste_text1(file, path_yes)
                    else:
                        results = ','.join((results, yes))
                        results = ','.join((results, 'NONE'))
                        path_yes = path + '/' + str(keyword) + '/' + keyword + '_No'
                        if not os.path.exists(path_yes):
                            os.makedirs(path_yes)
                        copy_paste_text1(file, path_yes)
                    text = text_exp
                    if keyword == keywords_range[0] and sent_range != []:
                        range_Yes_No[0].append(sent_range)
                        Range = True
                    elif keyword == keywords_range[1] and sent_range != []:
                        range_Yes_No[1].append(sent_range)
                        Range = True
                    elif keyword == keywords_range[2] and sent_range != []:
                        range_Yes_No[2].append(sent_range)
                        Range = True
                if Range == True:
                    r += 1
                a += 1
                all_results.append(results)

    return all_results, range_Yes_No


def Save_results(results, path):
    """
    :param results: results of mentioning the keywords in the text or not from Check_Keywords_CSV function
    :param path: the path to save the excel file
    """
    keywords = ['Electrode composition', 'Electrolyte composition', 'Separator', 'Electrode surface area',
                'Electrode thickness', 'Slurry casting method', 'Electrolyte volume',
                'Electrode porosity', 'Mass loading', 'Current density', 'Cutoff voltage']
    xlsx_path = path + '\Outputs.xlsx'
    workbook = xlsxwriter.Workbook(xlsx_path)
    worksheet = workbook.add_worksheet()
    row = 0
    worksheet.write(row, 1, 'Year')
    col = 2
    for item in keywords:
        worksheet.write(row, col, item)
        col += 1
        worksheet.write(row, col, 'Range of values Yes or Not')
        col += 1
    row = 1
    for result in results:
        result_split = result.split(',')
        for i in range(0, len(result_split)):
            worksheet.write(row, i, result_split[i])
        row += 1
    workbook.close()


def Save_results_range(results, path):
    """
    :param results: results of range or exact value from Check_Keywords_CSV function
    :param path: the path to save the excel file
    """
    keywords_range = ['Electrode thickness', 'Electrode porosity', 'Mass loading']
    for i in range(len(keywords_range)):
        xlsx_path = path + '\Outputs_Range_' + str(keywords_range[i]) + '.xlsx'
        workbook = xlsxwriter.Workbook(xlsx_path)
        worksheet = workbook.add_worksheet()
        row = 0
        col = 0
        for item in keywords_range:
            worksheet.write(row, col, 'Articles')
            col += 1
            worksheet.write(row, col, item)
            col += 1
            worksheet.write(row, col, 'Exact/Range')
            row = 1
            col = 0
            a = 1
            result = results[i]
            for article in result:
                sents_articles = article
                sents_articles.sort()
                sents_articles = list(k for k, _ in itertools.groupby(sents_articles))
                for sent in sents_articles:
                    worksheet.write(row, col, 'Article ' + str(a))
                    col += 1
                    worksheet.write(row, col, sent[0])
                    col += 1
                    worksheet.write(row, col, sent[1])
                    row += 1
                    col = 0
                a += 1
            workbook.close()


######################## Convert PDFs to TXTs ##########################################
def Converting_From_PDF_OR_XML_To_TXT(Path_To_PDFs, Path_To_TXTs):
    """
    :param Path_To_PDFs: path to all PDFs or XMLs
    :param Path_To_TXTs: the path to save the TXT format
    """
    Converting_Function(Path_To_PDFs, Path_To_TXTs)


################# Filtring Function and Cheking the keywords ######################################
def Filtring_And_Checking_Keywords(Path_To_TXTs):
    """
    :param Path_To_TXTs: the path to all TXTs
    :return: Save results as excel file
    """
    files_short = np.array([f for f in os.listdir(Path_To_TXTs) if os.path.isfile(os.path.join(Path_To_TXTs, f))])
    files = np.array([Path_To_TXTs + '/' + f for f in files_short])
    Filtring_Function(files, Path_To_TXTs)
    ###########################################################################
    batteries = ['Lithium Ion Battery', 'Sodium Ion Battery']
    for battery in batteries:
        temp_path = Path_To_TXTs + '/' + battery
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        results, range_Yes_No = Check_Keywords_CSV(temp_path)
        Save_results(results, temp_path)
        Save_results_range(range_Yes_No, temp_path)
