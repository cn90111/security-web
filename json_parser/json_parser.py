# -*- coding: UTF-8 -*-

import json
import math
import re
import pandas as pd
from django.utils.translation import gettext
from general.exception import NotAddressException
from general.function import ContentDetection

class JsonParser():

    __n_parts = 10
    __float_accuracy = 4
    __tw_address_accuracy_pattern = '縣市鄉鎮市區街路村里巷弄號樓室'
    
    def get_interval(self, number_list):
        detection = ContentDetection()
        if not detection.is_number(number_list):
            raise TypeError(number_list + 'is not number list')
        number_list = list(filter(None, number_list))
        number_list_is_float = detection.is_float(number_list)
        if number_list_is_float:
            min_value = float(min(number_list))
            max_value = float(max(number_list))
        else:
            min_value = int(min(number_list))
            max_value = int(max(number_list))
            
        interval = []
        gap = (max_value - min_value) / self.__n_parts
        if number_list_is_float:
            for i in range(self.__n_parts):
                upper_limit = round(min_value + gap*(i+1), self.__float_accuracy)
                lower_limit = round(min_value + gap*i, self.__float_accuracy)
                interval.append([lower_limit, upper_limit])
        else:
            for i in range(self.__n_parts):
                upper_limit = round(min_value + gap*(i+1))
                lower_limit = round(min_value + gap*i)
                interval.append([lower_limit, upper_limit])
        return interval
        
    def get_unrelated_structure(self, string_list, ancestor):
        genealogy = {}
        for item in string_list:
            genealogy[item] = ancestor
        genealogy[ancestor] = ancestor
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
        pattern = '[^'+self.__tw_address_accuracy_pattern+']*'+\
                    '['+self.__tw_address_accuracy_pattern+']'
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
        detection = ContentDetection()
        if detection.is_string(column):
            return list(filter(None, list(set(column))))
        else:
            return None
        
    def get_file_string_element(self, file_path):
        dataframe = pd.read_csv(file_path, keep_default_na=False)
        column_element = {}
        for column_title in dataframe:
            element = self.get_column_element(dataframe.loc[:, column_title].values.tolist())
            if element:
                column_element[column_title] = element
        return column_element
                
    def parser_to_json(self, file_path, structure, **kwargs):
        json_dict = {}
        detection = ContentDetection()
        dataframe = pd.read_csv(file_path, keep_default_na=False)
        print(dataframe)
        number_title_pair_dict = None
        interval_dict = None
        if 'number_title_pair_dict' in kwargs:
            number_title_pair_dict = kwargs.get('number_title_pair_dict')
            interval_dict = kwargs.get('interval_dict')
        for column_title in dataframe:
            temp = {}
            column = dataframe.loc[:, column_title].values.tolist()
            if detection.is_string(column):
                temp['type'] = 'categorical'
                temp['structure'] = structure[column_title]
            elif detection.is_number(column):
                temp['type'] = 'numerical'
                temp['min'] = min(column)
                temp['max'] = max(column)
                
                if detection.is_float(column):
                    temp['num_type'] = 'float'
                else:
                    temp['num_type'] = 'int'
                    
                if number_title_pair_dict and number_title_pair_dict[column_title] == 'number':
                    interval = []
                    value_list = interval_dict[column_title]
                    for i in range(len(value_list)-1):
                        interval.append([value_list[i], value_list[i+1]])
                    temp['interval'] = interval
                else:
                    temp['interval'] = self.get_interval(column)
            else:
                temp['type'] = 'categorical'
                temp['structure'] = {'':''}
            json_dict[column_title] = temp
        return json_dict
    
    def parser_to_DPView_json(self, file_path, pair_dict, **kwargs):
        json_dict = {}
        detection = ContentDetection()
        dataframe = pd.read_csv(file_path, keep_default_na=False)
        interval_dict = None
        if 'interval_dict' in kwargs:
            interval_dict = kwargs.get('interval_dict')
        for column_title in dataframe:
            temp = {}
            column = dataframe.loc[:, column_title].values.tolist()
            if detection.is_string(column):
                temp['type'] = 'cat'
            elif detection.is_number(column):
                if pair_dict[column_title] == 'number':
                    temp['type'] = 'num'
                elif pair_dict[column_title] == 'single':
                    temp['type'] = 'single'
                elif pair_dict[column_title] == 'category':
                    temp['type'] = 'num2cat'
                if interval_dict and pair_dict[column_title] == 'number':
                    interval = []
                    value_list = interval_dict[column_title]
                    for i in range(len(value_list)-1):
                        interval.append([value_list[i], value_list[i+1]])
                    temp['bucket'] = interval
                else:
                    temp['bucket'] = self.get_interval(column)
            else:
                temp['type'] = 'single'
            json_dict[column_title] = temp
        return json_dict
        
    def create_json_file(self, file_path, file_name, structure_mode, structure_dict, **kwargs):
        for key in structure_mode:
            mode = structure_mode[key]
            if mode == 'tw_address':
                structure_dict[key] = \
                    self.get_tw_address_structure(structure_dict[key].keys())
                if not structure_dict[key]:
                    raise NotAddressException(key + gettext("欄位所存資料並非地址，請重新填寫"))
            elif mode == 'us_address':
                structure_dict[key] = \
                    self.get_us_address_structure(structure_dict[key].keys())
                if not structure_dict[key]:
                    raise NotAddressException(key + gettext("欄位所存資料並非地址，請重新填寫"))
            elif mode == 'unrelated':
                structure_dict[key] = \
                    self.get_unrelated_structure(structure_dict[key].keys(), key)            
            if not structure_dict[key]:
                raise Exception(key + gettext("欄位所生成的配對資料為空"))
        directory_name = file_name.split(".")[-2]
        file_path = file_path + directory_name + '/'
        json_path = file_path + directory_name + '_dict.json'
        if 'number_title_pair_dict' in kwargs:
            json_object = json.dumps(self.parser_to_json\
                (file_path+file_name, structure_dict,
                number_title_pair_dict=kwargs.get('number_title_pair_dict'),
                interval_dict=kwargs.get('interval_dict')))
        else:
            json_object = json.dumps(self.parser_to_json\
                                (file_path+file_name, structure_dict))
        with open(json_path, 'w') as file:
            file.write(json_object)
            
    def create_DPView_json_file(self, file_path, file_name, pair_dict, **kwargs):
        directory_name = file_name.split(".")[-2]
        file_path = file_path + directory_name + '/'
        json_path = file_path + directory_name + '_dict.json'
        if 'interval_dict' in kwargs:
            json_object = json.dumps(self.parser_to_DPView_json\
                (file_path+file_name, pair_dict,
                interval_dict=kwargs.get('interval_dict')))
        else:
            json_object = json.dumps(self.parser_to_DPView_json\
                (file_path+file_name, pair_dict))
        with open(json_path, 'w') as file:
            file.write(json_object)