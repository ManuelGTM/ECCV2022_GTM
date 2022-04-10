import pympi
import os
import argparse

def create_folder(folder):
    print ('create_folder: {}'.format(folder))    
    try:
        os.makedirs(folder)    
        print("Directory " , folder ,  " Created ")
    except FileExistsError:
        print("Directory " , folder ,  " already exists")
        
def eaf_get_list_anns(path_folder_eaf):
    lst_files = os.listdir(path_folder_eaf)
    list_anns = []
    for elan_file in lst_files:
        if '.eaf' in elan_file:
            filepath_in = os.path.join(path_folder_eaf, elan_file)
            eafob = pympi.Elan.Eaf(filepath_in)
            ort_tier_names=list(eafob.get_tier_names())
            for annotation in eafob.get_annotation_data_for_tier(ort_tier_names[0]):
                # print (annotation)
                try:
                    label = annotation[2].replace('*','')
                    if label not in list_anns:
                        list_anns.append(label)
                except:
                    print('exception')
                    pass
    print ('return {} elements'.format(len(list_anns)))
    return list_anns
    
def main(args):
       
    folder_in =args.input
    print (eaf_get_list_anns(folder_in))


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Generate Result Output')
    parser.add_argument('--input', required=True, default='', type=str)
    arg = parser.parse_args()
    main(arg)


# python get_labels_eaf.py --input /home/temporal2/mvazquez/Challenge/utils_eaf/data/9ABR/ANOTADOS_cut
# python get_labels_eaf.py --input /home/temporal2/mvazquez/Challenge/utils_eaf/data/9ABR/ANOTADOS_TRACK1_cut
# python get_labels_eaf.py --input /home/temporal2/mvazquez/Challenge/utils_eaf/data/9ABR/ANOTADOS_TRACK2_cut