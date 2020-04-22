# -*- coding: UTF-8 -*-

from json_parser.json_parser import JsonParser

import unittest
import json
import csv
import os
import pandas as pd

# Create your tests here.

class TestParser(unittest.TestCase):
    
    csv_path = 'test.csv'
    json_parser = JsonParser()
    
    @classmethod
    def setUpClass(cls):
        with open(cls.csv_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['String','Integer','String2','Float'])
            writer.writerow(['a','1','x','1.1'])
            writer.writerow(['b','22','y','22.22'])
            writer.writerow(['c','333','x','333.333'])
            
        cls.df = pd.read_csv(cls.csv_path)
        cls.categorical = cls.df.loc[:, 'String'].values.tolist()
        cls.number_int = cls.df.loc[:, 'Integer'].values.tolist()
        cls.number_float = cls.df.loc[:, 'Float'].values.tolist()
        cls.mixing = ['a',2,'c',4,'d']
        cls.empty = []
       
    @classmethod       
    def tearDownClass(cls):
        try:
            os.remove(cls.csv_path)
        except OSError as e:
            print(e)
        else:
            print("Test file is deleted successfully")
    
    def test_is_string(self):
        self.assertTrue(self.json_parser.is_string(self.categorical))
        self.assertFalse(self.json_parser.is_string(self.number_int))
        self.assertFalse(self.json_parser.is_string(self.number_float))
        self.assertFalse(self.json_parser.is_string(self.mixing))
        self.assertFalse(self.json_parser.is_string(self.empty))

    def test_is_number(self):
        self.assertFalse(self.json_parser.is_number(self.categorical))
        self.assertTrue(self.json_parser.is_number(self.number_int))
        self.assertTrue(self.json_parser.is_number(self.number_float))
        self.assertFalse(self.json_parser.is_number(self.mixing))
        self.assertFalse(self.json_parser.is_number(self.empty))
        
    def test_is_float(self):
        self.assertFalse(self.json_parser.is_float(self.categorical))
        self.assertFalse(self.json_parser.is_float(self.number_int))
        self.assertTrue(self.json_parser.is_float(self.number_float))
        self.assertFalse(self.json_parser.is_float(self.mixing))
        self.assertFalse(self.json_parser.is_float(self.empty))
    
    def test_calculate_interval(self):
        number_int_interval = self.json_parser.get_interval(self.number_int)
        number_float_interval = self.json_parser.get_interval(self.number_float)
        
        test_int_interval = [[1,35],[35,69],\
                            [69,103],[103,137],\
                            [137,171],[171,205],\
                            [205,239],[239,273],\
                            [273,307],[307,341]]
        
        test_float_interval = [[1.1,34.3233],[34.3233,67.5466],\
                                [67.5466,100.7699],[100.7699,133.9932],\
                                [133.9932,167.2165],[167.2165,200.4398],\
                                [200.4398,233.6631],[233.6631,266.8864],\
                                [266.8864,300.1097],[300.1097,333.333]]
        
        for i in range(len(number_int_interval)):
            for j in range(len(number_int_interval[i])):
                self.assertEqual\
                    (number_int_interval[i][j], test_int_interval[i][j])
        
        for i in range(len(number_float_interval)):
            for j in range(len(number_float_interval[i])):
                self.assertAlmostEqual\
                    (number_float_interval[i][j], test_float_interval[i][j])
                    
        with self.assertRaises(Exception):
            self.json_parser.get_interval(self.categorical)
            self.json_parser.get_interval(self.mixing)
            self.json_parser.get_interval(self.empty)
    
    def test_unrelated_structure(self):
        test_structure = {'String':'String', 'a':'String', 'b':'String', 'c':'String'}
        structure = self.json_parser.get_unrelated_structure(self.categorical, 'String')
        for key in structure.keys():
            self.assertEqual(structure.get(key), test_structure.get(key))
        
    def test_tw_address_structure(self):
        test_structure = {'台北市大安區忠孝東路100號':'台北市大安區忠孝東路',\
                        '台中市清水區護岸路123號':'台中市清水區護岸路',\
                        '台中市南區學府路16號':'台中市南區學府路',\
                        '台北市大安區忠孝東路':'台北市大安區',\
                        '台中市清水區護岸路':'台中市清水區',\
                        '台中市南區學府路':'台中市南區',\
                        '台北市大安區':'台北市',\
                        '台中市清水區':'台中市',\
                        '台中市南區':'台中市',\
                        '台北市':'台北市',\
                        '台中市':'台中市'}
                        
        address_list = ['台北市大安區忠孝東路100號',\
                        '台中市清水區護岸路123號',\
                        '台中市南區學府路16號']
                        
        structure = self.json_parser.get_tw_address_structure(address_list)
        
        for key in structure.keys():
            self.assertEqual(structure.get(key), test_structure.get(key))

    def test_us_address_structure(self):
        test_structure = {'678 Montgomery St, Jersey City, NJ 07306':'Jersey City, NJ 07306',\
                        '30 Mall Dr W, Jersey City, NJ 07310':'Jersey City, NJ 07310',\
                        '75 Grasslands Rd, Valhalla, NY 10595':'Valhalla, NY 10595',\
                        'Jersey City, NJ 07306':'NJ 07306',\
                        'Jersey City, NJ 07310':'NJ 07310',\
                        'Valhalla, NY 10595':'NY 10595',\
                        'NJ 07306':'NJ',\
                        'NJ 07310':'NJ',\
                        'NY 10595':'NY',\
                        'NJ':'NJ',\
                        'NY':'NY'}
                        
        address_list = ['678 Montgomery St, Jersey City, NJ 07306',\
                        '30 Mall Dr W, Jersey City, NJ 07310',\
                        '75 Grasslands Rd, Valhalla, NY 10595']
                        
        structure = self.json_parser.get_us_address_structure(address_list)
        
        for key in structure.keys():
            self.assertEqual(structure.get(key), test_structure.get(key))
    
    def test_split_tw_address(self):
        test_split = [['台北市','大安區','忠孝東路','100號'],\
                        ['台中市','清水區','護岸路','123號'],\
                        ['台中市','南區','學府路','16號']]
                        
        address_list = ['台北市大安區忠孝東路100號',\
                        '台中市清水區護岸路123號',\
                        '台中市南區學府路16號']
        split_list = []
        for address in address_list:
            split_list.append(self.json_parser.split_tw_address(address))
        for i in range(len(split_list)):
            for j in range(len(split_list[i])):
                self.assertEqual(split_list[i][j], test_split[i][j])
    
    def test_get_file_string_element(self):
        test_element = {'String':{'a','b','c'},'String2':{'x','y'}}
        file_string_element = self.json_parser.get_file_string_element(self.csv_path)
        for column_name in file_string_element.keys():
            self.assertEqual(file_string_element[column_name],\
                                test_element[column_name])
        
    def test_get_column_element(self):
        column = ['a','r','d','a','d']
        test_element = {'a','r','d'}
        element = self.json_parser.get_column_element(column)
        self.assertEqual(element, test_element)
    
    def test_parser_to_json(self):
        test_json = {
                        'String':{
                            'type':'categorical',
                            'structure':{
                                'String':'String',
                                'a':'String',
                                'b':'String',
                                'c':'String'
                            }
                        },
                        'Integer':{
                            'type':'numerical', 
                            'min':1, 
                            'max':333, 
                            'num_type':'int',
                            'interval':[[1,35],[35,69],\
                            [69,103],[103,137],\
                            [137,171],[171,205],\
                            [205,239],[239,273],\
                            [273,307],[307,341]]
                        },
                        'String2':{
                            'type':'categorical',
                            'structure':{
                                'x':'x',
                                'y':'x'
                            }
                        },
                        'Float':{
                            'type':'numerical', 
                            'min':1.1, 
                            'max':333.333, 
                            'num_type':'float',
                            'interval':[[1.1,34.3233],[34.3233,67.5466],\
                                [67.5466,100.7699],[100.7699,133.9932],\
                                [133.9932,167.2165],[167.2165,200.4398],\
                                [200.4398,233.6631],[233.6631,266.8864],\
                                [266.8864,300.1097],[300.1097,333.333]]
                        }
                    }
        test_json_string = json.dumps(test_json)
        structure = {
                        'String':{
                            'String':'String',
                            'a':'String',
                            'b':'String',
                            'c':'String'
                        },
                        'String2':{
                            'x':'x',
                            'y':'x'
                        },
                    }
        json_string = json.dumps(self.json_parser.parser_to_json\
                                (self.csv_path, structure))
        
        self.assertEqual(test_json_string,json_string)
    
if __name__ == '__main__':
    unittest.main()
