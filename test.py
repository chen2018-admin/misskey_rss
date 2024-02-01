"""
-*- coding: utf-8 -*-

@Author : geteshi
@Time : 2024/2/1 10:22
@File : test.py
"""
import yaml
import os

path = os.path.join(os.path.dirname(__file__), "sources.yaml")
data = yaml.safe_load(open(path, 'r', encoding="utf-8"))
print(data)
