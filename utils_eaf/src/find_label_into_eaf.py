import pympi
import os
import argparse
import datetime
import numpy as np

def create_folder(folder):
    print ('create_folder: {}'.format(folder))    
    try:
        os.makedirs(folder)    
        print("Directory " , folder ,  " Created ")
    except FileExistsError:
        print("Directory " , folder ,  " already exists")
        
def format_milliseconds_HH_MM_SS_MS(milliseconds):
    return datetime.timedelta(milliseconds=int(milliseconds))
        
            
def eaf_seach_annotation(path_folder_eaf, annotation_searched):
    lst_files = os.listdir(path_folder_eaf)
    
    intervals = []
    list_filenames = []
    for elan_file in lst_files:
        if '.eaf' in elan_file:
            filepath_in = os.path.join(path_folder_eaf, elan_file)
            eafob = pympi.Elan.Eaf(filepath_in)
            ort_tier_names=list(eafob.get_tier_names())

            for annotation in eafob.get_annotation_data_for_tier(ort_tier_names[0]):
                try:
                    label = annotation[2].replace('*','')
                    if label ==  annotation_searched:
                        line = 'find {} in {} interval {} - {}'.format(annotation, filepath_in, format_milliseconds_HH_MM_SS_MS(annotation[0]), format_milliseconds_HH_MM_SS_MS(annotation[1]))
                        filename = elan_file.replace('.eaf','')
                        entry = np.array([filename,annotation[0], annotation[1]])
                        intervals.append(entry)
                        print(line)
                        
                        if filename not in list_filenames:
                            list_filenames.append(filename)
                except:
                    print('exception')
                pass
        
    return np.asarray(intervals), list_filenames
    
def main(args):
       
    folder_in =args.input
    label =args.label
    
    arr_intervals, list_filenames= eaf_seach_annotation(folder_in, label)
    
    print ('arr_intervals')
    print (arr_intervals)
        
    print ('list_filenames')
    print (list_filenames)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Generate Result Output')
    parser.add_argument('--input', required=True, default='', type=str)
    parser.add_argument('--label', required=True, default='', type=str)
    arg = parser.parse_args()
    main(arg)


# python find_label_into_eaf.py --input /home/temporal2/mvazquez/Challenge/utils_eaf/data/8ABR/eaf --label :