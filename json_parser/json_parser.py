# -*- coding: UTF-8 -*-

import json
import math
import re
import pandas as pd

class JsonParser():
    
    __n_parts = 10
    __float_accuracy = 4
    __tw_address_accuracy_pattern = '縣市鄉鎮市區街路村里巷弄號樓室'

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
            upper_limit = round(min_value + gap*(i+1), self.__float_accuracy)
            lower_limit = round(min_value + gap*i, self.__float_accuracy)
            interval.append([lower_limit, upper_limit])
        return interval
        
    def get_unrelated_structure(self, string_list, ancestor):
        genealogy = {}
        for item in string_list:
            genealogy[item] = ancestor
        print('genealogy ',genealogy)
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
        pattern = '[^'+self.__tw_address_accuracy_pattern+']*\
                    ['+self.__tw_address_accuracy_pattern+']'
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
    
    def get_column_element(self, column):
        if self.is_string(column):
            return list(set(column))
        else:
            return None
        
    def get_file_string_element(self, file_path):
        dataframe = pd.read_csv(file_path)
        column_element = {}
        for column_title in dataframe:
            element = self.get_column_element(dataframe.loc[:, column_title].values.tolist())
            if element:
                column_element[column_title] = element
        return column_element
                
    def parser_to_json(self, file_path, structure):
        json_dict = {}
        dataframe = pd.read_csv(file_path)
        for column_title in dataframe:
            temp = {}
            column = dataframe.loc[:, column_title].values.tolist()
            if self.is_string(column):
                temp['type'] = 'categorical'
                temp['structure'] = structure[column_title]
            elif self.is_number(column):
                temp['type'] = 'numerical'
                temp['min'] = min(column)
                temp['max'] = max(column)
                if self.is_float(column):
                    temp['num_type'] = 'float'
                else:
                    temp['num_type'] = 'int'
                temp['interval'] = self.get_interval(column)
            json_dict[column_title] = temp
        return json_dict
        
    def create_json_file(self, file_path, csv_file_name, structure_mode, structure_dict):
        for key in structure_mode:
            mode = structure_mode[key]
            if mode == 'tw_address':
                structure_dict[key] = \
                    self.get_tw_address_structure(structure_dict[key].keys())
            elif mode == 'us_address':
                structure_dict[key] = \
                    self.get_us_address_structure(structure_dict[key].keys())
            elif mode == 'unrelated':
                structure_dict[key] = \
                    self.get_unrelated_structure(structure_dict[key].keys(), key)
        directory_name = csv_file_name.split(".")[-2]
        file_path = file_path + directory_name + '/'
        json_path = file_path + directory_name + '_dict.json'
        json_object = json.dumps(self.parser_to_json\
                            (file_path+csv_file_name, structure_dict))
        with open(json_path, 'w') as file:
            file.write(json_object)