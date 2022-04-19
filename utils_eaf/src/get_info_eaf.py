from numpy import append
import pympi
import os
import argparse
import json
        
def eaf_get_list_anns(path_folder_eaf, asterisk, spaces):
    lst_files = os.listdir(path_folder_eaf)
    info_annotations = {}
    list_filenames=[]
    list_labels=[]
    
    info_annotations['labels'] = []
    info_annotations['filenames'] = []
    
    for elan_file in lst_files:
        if '.eaf' in elan_file:
            filepath_in = os.path.join(path_folder_eaf, elan_file)
            eafob = pympi.Elan.Eaf(filepath_in)
            ort_tier_names=list(eafob.get_tier_names())
            
            filename = elan_file.replace('.eaf','')
            
            list_filenames.append(filename)
            
            for annotation in eafob.get_annotation_data_for_tier(ort_tier_names[0]):
                print (annotation)
                try:
                    label = annotation[2]
                    if spaces:
                        label = label.replace(' ','')
                    if asterisk:
                        label = label.replace('*','')
                    
                    print(label)
                    
                    
                    if label not in list_labels:
                        list_labels.append(label)

                    print(filename)
                    if label in list(info_annotations.keys()):
                        if not filename in info_annotations[label]['files']:
                            info_annotations[label]['files'].append(filename)
                        info_annotations[label]['counter'] = info_annotations[label]['counter'] + 1
                    else:
                        info_annotations[label]={
                            'counter' : 1,
                            'files' : [],
                        }
                        info_annotations[label]['files'].append(filename)
                except:
                    print('exception')
                    pass
        
        info_annotations['labels'] = list_labels
        info_annotations['filenames'] = list_filenames
        
    return info_annotations
    
def main(args):
       
    folder_in =args.input
    file_out =args.output
    rm_asterisk =args.rm_asterisk
    rm_spaces =args.rm_spaces
    
    print ('return Data annotations')
    dict_eaf_info = eaf_get_list_anns(folder_in, rm_asterisk, rm_spaces)
    
    with open(file_out, "w") as outfile:
        json.dump(dict_eaf_info, outfile)
    
    print (dict_eaf_info)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Generate Result Output')
    parser.add_argument('--input', required=True, default='', type=str)
    parser.add_argument('--output', required=True, default='', type=str)
    parser.add_argument('--rm_asterisk', action='store_true')
    parser.add_argument('--rm_spaces', action='store_true')
    arg = parser.parse_args()
    main(arg)


# python get_info_eaf.py --input /home/temporal2/mvazquez/Challenge/utils_eaf/data/9ABR/ANOTADOS_TRACK1_cut --output /home/temporal2/mvazquez/Challenge/utils_eaf/data/18ABR/INFO/ANOTACION_MARUXA --rm_asterisk --rm_spaces
