# -*- coding: UTF-8 -*-

import json_parser

import unittest
import json
import csv
import os
import pandas as pd

# Create your tests here.

class TestParser(unittest.TestCase):
    
    csv_path = 'test.csv'
    
    @classmethod
    def setUpClass(cls):
        with open(cls.csv_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['String','Integer','Float'])
            writer.writerow(['a','1','1.1'])
            writer.writerow(['b','22','22.22'])
            writer.writerow(['c','333','333.333'])
            
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
    

    def test_is_categorical(self):
        self.assertTrue(json_parser.is_categorical(self.categorical))
        self.assertFalse(json_parser.is_categorical(self.number_int))
        self.assertFalse(json_parser.is_categorical(self.number_float))
        self.assertFalse(json_parser.is_categorical(self.mixing))
        self.assertFalse(json_parser.is_categorical(self.empty))

    def test_is_numerical(self):
        self.assertFalse(json_parser.is_numerical(self.categorical))
        self.assertTrue(json_parser.is_numerical(self.number_int))
        self.assertTrue(json_parser.is_numerical(self.number_float))
        self.assertFalse(json_parser.is_numerical(self.mixing))
        self.assertFalse(json_parser.is_numerical(self.empty))
    
    def test_get_max(self):
        self.assertEqual(json_parser.get_max(self.number_int), 333)
        self.assertEqual(json_parser.get_max(self.number_float), 333.333)
        with self.assertRaises(TypeError):
            json_parser.get_max(self.categorical)
        with self.assertRaises(TypeError):
            json_parser.get_max(self.mixing)
    
    def test_get_min(self):
        self.assertEqual(json_parser.get_min(self.number_int),1)
        self.assertEqual(json_parser.get_min(self.number_float),1.1)
        with self.assertRaises(TypeError):
            json_parser.get_max(self.categorical)
        with self.assertRaises(TypeError):
            json_parser.get_max(self.mixing)
            
    def test_calculate_interval(self):
        number_int_interval = json_parser.get_interval(self.number_int)
        number_float_interval = json_parser.get_interval(self.number_float)
        
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
        structure = json_parser.get_unrelated_structure(self.categorical, 'String')
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
                        
        structure = json_parser.get_tw_address_structure(address_list)
        
        for key in structure.keys():
            self.assertEqual(structure.get(key), test_structure.get(key))

if __name__ == '__main__':
    unittest.main()
