# -*- coding: utf-8 -*-
"""
Created on Tue May  2 09:13:04 2023

@author: 11107045
"""
import xmltodict

with open('05153465.xml', 'r', encoding="utf-8") as f:
    data = f.read()
record = xmltodict.parse(data)
Postxml = record['cdp:ContentPackage']['cdp:ContentContainer']['cdp:StructuredContent']['ClinicalDocument']