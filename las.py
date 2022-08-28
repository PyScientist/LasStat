def read_file(las_path):
    """Read file to following decomposition
    return list of strings"""
    file_to_procces = open(las_path, 'r')
    strings_in_file = file_to_procces.readlines()
    file_to_procces.close()
    return strings_in_file


def search_first_data_block_string(prefix, strings_in_file):
    """Search the first string of data block with given prefix"""
    position = 'Novalue'
    for x in range(len(strings_in_file)):
        if str(strings_in_file[x]).startswith(prefix) == 1:
            print(strings_in_file[x].startswith(prefix))
            position = x
            break
    return position


def single_block(position, strings_in_file):
    """"Combine single data block by its position"""
    data_block = []
    if (position)!='Novalue':
        for x in range(position+1, len(strings_in_file)) :         
            if strings_in_file[x].startswith("~") == 0:
                if strings_in_file[x].startswith("#") == 0:
                    data_block.append(strings_in_file[x].strip())
            else:
                break
    return data_block
    
    
def combine_data_bloks(las_path):
    """Prepare the set of datablocks"""
    prefix_datablock_list=['~V', '~W', '~C', '~P', '~O', '~A', '~B']
    strings_in_file  = read_file(las_path)
    data_blocks = []
    
    for prefix in range(len(prefix_datablock_list)):
        position = search_first_data_block_string(prefix_datablock_list[prefix], strings_in_file)
        data_block = single_block(position, strings_in_file)
        data_blocks.append(data_block)
    print('exists')
    return data_blocks
    

if __name__ == '__main__':
     las_path = './las_test/115_БКЗ.las'
     content = combine_data_bloks(las_path)
     print(content)