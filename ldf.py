#!/usr/bin/env python
# coding: utf-8

import xml.etree.ElementTree as ET
import pandas as pd
import os
from scipy.integrate import simps
from const import *

from plotting import *


def conv_to_ndarr(inputs):
    return map(lambda x:np.array(x), inputs)


class parser:
    
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
        #ldf_files.sort(key=lambda x:float(x.split('/')[-1][:-4]))
        return ldf_files

class processor():
    def __init__(self, IV):
        self.IV = IV
        self.V = np.array(IV['V'])
        self.I = np.array(IV['I'])
        
    def cal_sat(self):
        return -self.V[0], -self.I[0]

    def cal_Vp(self):
        dIdV = np.gradient(self.I, self.V)
        self.dIdV = dIdV
        Vp = self.V[np.argmax(dIdV)]
        return Vp
        
    def cal_second_derivative(self):
        dIdV = np.gradient(self.I, self.V)
        ddI = np.gradient(dIdV, self.V)
        return self.V, ddI
        
    def cal_eepf(self):
        Vp = self.cal_Vp()
    
        I_adj = self.I[self.V<=Vp]
        V_adj = self.V[self.V<=Vp] - Vp
        dI = np.gradient(I_adj, V_adj)
        ddI = np.gradient(dI, V_adj)
        
        self.eedf = 2*ddI/e/Ap*np.sqrt(2*Me*(Vp-V_adj)/e)
        self.eepf = self.eedf/np.sqrt(Vp-V_adj)
        self.V_adj = np.flip(-V_adj)
        self.eepf = np.flip(self.eepf)
        self.eedf = np.flip(self.eedf)
        return self.V_adj, self.eepf, self.eedf

    def cal_ne(self, V_lim):
        mask = self.V_adj < V_lim
        reduced_eepf = self.eepf[mask]
        reduced_V = self.V_adj[mask]
        return simps(reduced_eepf, reduced_V)

    def cal_Te(self, ne, V_lim):
        mask = self.V_adj < V_lim
        reduced_eedf = self.eedf[mask]
        reduced_V = self.V_adj[mask]
        return 2/3*simps(reduced_eedf/ne*reduced_V, reduced_V)