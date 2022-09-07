import numpy as np
from datetime import datetime

class CurveSet:
    strings_in_file = []
    data_blocks_dict = {}
    param_dict = {}
    curves_list = []
    units_list = []
    description_list = []
    curves_data  = np.array([])
    logger = []
    
    def __init__(self, las_path):
          self.las_path  = las_path
          self.read_file()
          self.combine_data_blocks()
          self.version_search()
          self.got_params()
          self.get_curve_spec_list()
          self.got_data()
          self.fix_noval()
          #self.printstat()
          
    def read_file(self):
           """Read file to following decomposition
           return list of strings"""
           file_to_procces = open(self.las_path, 'r')
           self.strings_in_file = file_to_procces.readlines()
           file_to_procces.close()
           
    def search_first_data_block_string(self, prefix):
            """Search the first string of data block with given prefix
            and return it index (started from zero)"""
            position = None
            for x in range(len(self.strings_in_file)):
                  if self.strings_in_file[x].startswith(prefix) == True:
                     position = x
                     break
            return position

    def single_block(self, position):
            """"Combine single data block by its position"""
            data_block = []
            if (position)!=None:
               for x in range(position+1, len(self.strings_in_file)):
                     if self.strings_in_file[x].startswith("~") == False:
                        if self.strings_in_file[x].startswith("#") == False:
                           data_block.append(self.strings_in_file[x].strip())
                     else: break
                        
            return data_block
            
    def combine_data_blocks(self):
           """Prepare the set of datablocks by given prefixes"""
           prefix_datablock_list=['~V', '~W', '~C', '~P', '~O', '~A', '~B']          
           for prefix in prefix_datablock_list:
                 self.data_blocks_dict[prefix] = []
           for key in self.data_blocks_dict:                 
                 position = self.search_first_data_block_string(key)               
                 self.data_blocks_dict[key]=self.single_block(position)
    
    def printstat(self):
           print(self.param_dict)
           print(list(zip(self.curves_list, self.units_list, self.description_list)))
    
    def fix_noval(self):
           self.curves_data[self.curves_data==-9999.25] = np.nan
    
    @staticmethod
    def got_las_data(line, vers):
           """Get data from las 2.0 version"""
           length_line=len(line)
           mesto_pervoi_tochki=line.find('.')
           stroka_bez_nazvaniya=line[mesto_pervoi_tochki+1:length_line]
           mesto_probela=stroka_bez_nazvaniya.find(' ')
           mesto_dvoetochiya=stroka_bez_nazvaniya.find(':')
           if (vers == '1.20') or (vers == '1.2') or (vers == '1.200'):
              return line[line.find(':')+1:length_line].strip()
           elif (vers == '2.0') or (vers == '2.00') or (vers == '2'):
              return stroka_bez_nazvaniya[mesto_probela:mesto_dvoetochiya].strip()
           else: return "missing"
                                                                                                                                                                                                                                                                                                          
    def version_search(self):
           """Get las version"""           
           for line in self.data_blocks_dict['~V']:
                 if (line.startswith('VERS') == True) or (line.startswith('Vers') == True):
                     self.param_dict['version'] = self.got_las_data(line, '2.0')
                 if line.startswith('WRAP') == True:
                    self.param_dict['wrap'] = self.got_las_data(line, '2.0')

    def got_params(self):
          """Get noval sign, start and stop depth from 
          Well information block"""
          self.param_dict['noval'] = 'missing'
          self.param_dict['start'] = 'missing'
          self.param_dict['stop'] = 'missing'
          self.param_dict['step'] = 'missing'
          self.param_dict['well'] = 'missing'
          self.param_dict['uwi'] = 'missing'
          self.param_dict['date'] = 'missing'

          for line in self.data_blocks_dict['~W']:
               if line.startswith('NULL') == True:
                   self.param_dict['noval'] = self.got_las_data(line, '2')
               elif line.startswith('STRT') == True:
                   self.param_dict['start'] = self.got_las_data(line, '2')
               elif line.startswith('STOP') == True:
                   self.param_dict['stop'] = self.got_las_data(line, '2')
               elif line.startswith('STEP') == True:
                    self.param_dict['step'] = self.got_las_data(line, '2')
               elif line.startswith('WELL') == True:
                    self.param_dict['well'] = self.got_las_data(line, self.param_dict['version'])
               elif line.startswith('UWI') == True:
                    self.param_dict['uwi'] = self.got_las_data(line, self.param_dict['version'])
               elif line.startswith('DATE') == True:
                    self.param_dict['date'] = self.got_las_data(line, self.param_dict['version'])                                                                                                 

    def get_curve_spec_list(self):
           """Get logging list"""
           for line in self.data_blocks_dict['~C']:
                 self.curves_list.append(line[0:line.find(".")].strip())
                 self.description_list.append(line[line.find(":")+1:len(line)].strip())
                 self.units_list.append(line[line.find('.')+1:line.find(':')].strip())
     
    def got_data(self):
           lines = [] 
           for line in self.data_blocks_dict['~A']:
                 current_line = line.split()
                 if len(current_line) == len(self.curves_list):
                    for i in range(len(current_line)):
                        if current_line[i] == self.param_dict['noval']:
                           current_line[i] = '-9999.25'
                    lines.append(current_line)
           true_lenght = float(self.param_dict['stop'])-float(self.param_dict['start'])
           diff = (len(lines)-1)*float(self.param_dict['step']) - true_lenght
           if diff == 0:
               self.curves_data = np.array(lines).transpose().astype(np.float64)
               self.logger.append('good quality')
 
def perfomance_test(las_path):
      for i in range(10):
        start = datetime.now()
        for x in range(80):
              set1 = CurveSet(las_path)
        print(datetime.now()-start)

     
if __name__ == '__main__':
     las_path = './las_test/115_БКЗ.las'
     perfomance_test(las_path)
     #set1 = CurveSet(las_path)
     