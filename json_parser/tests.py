# -*- coding: UTF-8 -*-

import json_parser

import unittest
import json
import csv
import os
import pandas as pd

# Create your tests here.

class TestParser(unittest.TestCase):
    
    def __init__(self, name):
        self.csv_path = 'test.csv'
    
    @classmethod
    def setUpClass(cls):
        with open(csv_path, 'w', newline='') as csv_file:
            writer = csv.writer(file)
            writer.writerow(['String','Integer','Float'])
            writer.writerow(['a','1','1.1'])
            writer.writerow(['b','22','22.22'])
            writer.writerow(['c','333','333.333'])
            
            self.df = pd.read_csv(csv_path)
            self.categorical = df.loc['String'].values.tolist()
            self.number_int = df.loc['Integer'].values.tolist()
            self.number_float = df.loc['Float'].values.tolist()
            self.mixing = [a,2,c,4,d]
            self.empty = []
       
    @classmethod       
    def tearDownClass(cls):
        try:
            os.remove(csv_path)
        except OSError as e:
            print(e)
        else:
            print("Test file is deleted successfully")
    

    def test_is_categorical(self):
        self.assertTrue(josn_parser.is_categorical(categorical))
        self.assertFalse(josn_parser.is_categorical(number_int))
        self.assertFalse(josn_parser.is_categorical(number_float))
        self.assertFalse(josn_parser.is_categorical(mixing))
        self.assertFalse(josn_parser.is_categorical(empty))

    def test_is_numerical(self):
        self.assertFalse(josn_parser.is_numerical(categorical))
        self.assertTrue(josn_parser.is_numerical(number_int))
        self.assertTrue(josn_parser.is_numerical(number_float))
        self.assertFalse(josn_parser.is_numerical(mixing))
        self.assertFalse(josn_parser.is_numerical(empty))
    
    def test_get_max(self):
        self.assertEqual(josn_parser.get_max(number_int), 333)
        self.assertEqual(josn_parser.get_max(number_float), 333.333)
        with self.assertRaises(TypeError):
            josn_parser.get_max(categorical)
        with self.assertRaises(TypeError):
            josn_parser.get_max(mixing)
    
    def test_get_min(self):
        self.assertEqual(josn_parser.get_min(number_int),1)
        self.assertEqual(josn_parser.get_min(number_float),1.1)
        with self.assertRaises(TypeError):
            josn_parser.get_max(categorical)
        with self.assertRaises(TypeError):
            josn_parser.get_max(mixing)
            
    def test_calculate_interval(self):
        number_int_interval = josn_parser.get_interval(number_int)
        number_float_interval = josn_parser.get_interval(number_float)
        
        test_int_interval = [[1,36],[36,72],\
                            [72,108],[108,144],\
                            [144,180],[108,216],\
                            [216,252],[252,288],\
                            [288,324],[324,360]]
        
        test_float_interval = [[1.1,36.6553],[36.6553,72.2106],\
                                [72.2106,107.7659],[107.7659,143.3212],\
                                [143.3212,178.8765],[178.8765,214.4318],\
                                [214.4318,249.9871],[249.9871,285.5424],\
                                [285.5424,321.0977],[321.0977,356.653]]
        
        for i in len(number_int_interval):
            for j in  len(number_int_interval[i]):
                self.assertEqual\
                    (number_int_interval[i][j], test_int_interval[i][j])
        
        for i in len(number_float_interval):
            for j in  len(number_float_interval[i]):
                self.assertAlmostEqual\
                    (number_float_interval[i][j], test_float_interval[i][j])
    
    def test_unrelated_structure(self):
        test_structure = {'String':'String', 'a':'String', 'b':'String', 'c':'String'}
        structure = josn_parser.get_unrelated_structure(self.categorical, 'String')
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
                        
        structure = josn_parser.get_tw_address_structure(address_list)
        
        for key in structure.keys():
            self.assertEqual(structure.get(key), test_structure.get(key))

if __name__ == '__main__':
    unittest.main()