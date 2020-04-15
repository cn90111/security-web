# -*- coding: UTF-8 -*-

import json
import math
import re
import pandas as pd

class JsonParser():
    
    __n_parts = 10
    tw_address_accuracy_pattern = '縣市鄉鎮市區街路村里巷弄號樓室'

    def is_string(self, item_list):
        if not item_list:
            return False
        for item in item_list:
            if type(item) is not str and type(item) is not chr:
                return False
        return True
        
    def is_number(self, item_list):
        if not item_list:
            return False
        for item in item_list:
            if type(item) is not int and type(item) is not float:
                return False
        return True
    
    def is_float(self, item_list):
        if not self.is_number(item_list):
            return False
        for item in item_list:
            if type(item) is float:
                return True
        return False
    
    def get_interval(self, number_list):
        if not self.is_number(number_list):
            raise TypeError(number_list + 'is not number list')
        min_value = min(number_list)
        max_value = max(number_list)
        interval = []
        if(self.is_float(number_list)):
            gap = (max_value - min_value) / self.__n_parts
        else:
            gap = math.ceil((max_value - min_value) / self.__n_parts)
        for i in range(self.__n_parts):
            interval.append([min_value + gap*i, min_value + gap*(i+1)])
        return interval
        
    def get_unrelated_structure(self, string_list, ancestor):
        genealogy = {}
        for item in string_list:
            genealogy[item] = ancestor
        return genealogy
        
    def get_tw_address_structure(self, address_list):
        genealogy = {}
        for address in address_list:
            split_list = self.split_tw_address(address)
            key = ''
            temp = ''
            for token in split_list:
                key = key + token
                if temp:
                    genealogy[key] = temp
                else:
                    genealogy[key] = token
                temp = key
        return genealogy
        
    def split_tw_address(self, address):
        pattern = '[^'+self.tw_address_accuracy_pattern+']*\
                    ['+self.tw_address_accuracy_pattern+']'
        token_list = re.findall(pattern, address)
        return token_list
        
    def get_us_address_structure(self, address_list):
        genealogy = {}
        for address in address_list:
            token_list = re.split(',\s?', address)
            key = ''
            temp = ''
            for token in reversed(token_list):
                key = token + key
                if temp:
                    genealogy[key] = temp
                else:
                    city = re.split('\s',key)[0]
                    genealogy[city] = city
                    genealogy[key] = city
                temp = key
                key = ', ' + key
        return genealogy