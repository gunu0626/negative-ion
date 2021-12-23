#!/usr/bin/env python
# coding: utf-8

import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import os

class LDF:
    
    def __init__(self, dir_):
        self.dir = dir_
        
    ### Private method ####    
    def __is_ldf(self, filename):
        if filename.find('.ldf')>=0:
            return True
        else:
            return False    

    def __to_excel(self, DataFrames, file):
        excel_file = file.replace('.ldf','.xlsx')
        writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
        DataFrames[0].to_excel(writer, sheet_name='IV')
        DataFrames[1].to_excel(writer, sheet_name='eedf')
        DataFrames[2].to_excel(writer, sheet_name='result')
        writer.save()

    ### Pullic method ####    
    def pull_attr(self, file, need_return = False, file_save = False):
        """pull_attr(file, need_return=False, file_save=False)"""
    
        ldf_list = self.ldf_paths()
        tree = ET.parse(file)
        root = tree.getroot()
        scanData = root.find('scanData')
        eepf_data = scanData.find('eedf_data')
        IV_data = scanData.find('data')
        results = scanData.find('results')

        # I-V Curve data parsing
        I = np.array(list(map(float,IV_data[0].text[1:-1].split(';'))))
        V = np.array(list(map(float,IV_data[1].text[1:-1].split(';'))))
        std_I = np.array(list(map(float,IV_data[2].text[1:-1].split(';'))))
        std_V = np.array(list(map(float,IV_data[3].text[1:-1].split(';'))))
        try:
            # EEDF data parsing
            eepf = np.array(list(map(float,eepf_data[0].text[1:-1].split(';'))))
            eepf_error = np.array(list(map(float,eepf_data[1].text[1:-1].split(';'))))
            eepf_energy = np.array(list(map(float,eepf_data[3].text[1:-1].split(';'))))
        except:
            print("no eedf datas")
            eepf = []
            eepf_error = []
            eepf_energy = []

        # Result data parsing
        Ne = float(results.find('Ne').text)
        Te = float(results.find('kTe').text)
        eepf_Ne = float(results.find('eedf_Ne').text)
        eepf_Ne_error = float(results.find('eedf_Ne_error').text)
        eepf_Te = float(results.find('eedf_kTe').text)
        eepf_Te_error = float(results.find('eedf_kTe_error').text)
        Ni = float(results.find('Ni').text)
        Vf = float(results.find('Vf').text)
        Vp = float(results.find('Vp').text)
        Vp_error = float(results.find('Vp_error').text)
        Isat = float(results.find('isat').text)
        Vsat = float(results.find('Vsat').text)


        df_IV = pd.DataFrame({'V': V, 'I': I, 'std_V': std_V, 'std_I': std_I})
        df_eedf = pd.DataFrame({'eepf_energy': eepf_energy, 'eepf': eepf, 'eepf_error': eepf_error})
        df_result = pd.DataFrame({'Ne': [Ne], 'Te': [Te], 'eepf_Ne': [eepf_Ne], 'eepf_Ne_error': [eepf_Ne_error], 'eepf_Te': [eepf_Te], 'eepf_Te_error': [eepf_Te_error], 'Ni': [Ni], 'Vf': [Vf], 'Vp': [Vp], 'Vp_error': [Vp_error], 'Isat': [Isat], 'Vsat': [Vsat]})

        if file_save:
            self.__to_excel([df_IV, df_eedf, df_result], file)

        if need_return:
            return [df_IV, df_eedf, df_result]

        return 0
    def ldf_paths(self):
        ldf_files = []
        for root, directories, files in os.walk(self.dir):
            for name in files:
                if self.__is_ldf(os.path.join(root, name)):
                    ldf_files.append(os.path.join(root, name))
        return ldf_files