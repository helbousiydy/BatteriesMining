#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from KeyWordsExtractions.Current_Density import test_fonction_1_cd
from KeyWordsExtractions.Filtring_Functions import test_fonction_1_ff

__all__ = ['test_fonction_1_ei', 'test_fonction_2_ei']


def test_fonction_1_ei():

    print(np.array([1, 2]))
    return "ca marche"


def test_fonction_2_ei():

    print(test_fonction_1_ff())
    return 'ok'