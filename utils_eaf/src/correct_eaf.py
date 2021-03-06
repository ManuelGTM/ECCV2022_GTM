import pympi
import os
import argparse
import utils


    
def eaf_correction(path_folder_eaf, path_folder_eaf_ok, corrections, deletes):
    lst_files = os.listdir(path_folder_eaf)
    print('Number of files: {}'.format(len(lst_files)))

    for elan_file in lst_files:
        if '.eaf' in elan_file:
            filepath_in = os.path.join(path_folder_eaf, elan_file)
            filepath_out = os.path.join(path_folder_eaf_ok, elan_file)
            eafob = pympi.Elan.Eaf(filepath_in)
            ort_tier_names=list(eafob.get_tier_names())

            eafob_new = pympi.Elan.Eaf(filepath_in)
            eafob_new.remove_tier(ort_tier_names[0],clean=True)
            eafob_new.remove_tier(ort_tier_names[1],clean=True)
            eafob_new.add_tier(ort_tier_names[0])
            eafob_new.add_tier(ort_tier_names[1])

            for annotation in eafob.get_annotation_data_for_tier(ort_tier_names[0]):
                # print (annotation)
                try:
                    label = annotation[2].replace('*','')
                    if label in corrections.keys():
                        line = 'correction {} in {} change {} to {}'.format(annotation, filepath_in, label, corrections[label])
                        label = corrections[label]
                        print(line)

                    if label not in deletes:
                        eafob_new.add_annotation(ort_tier_names[0], annotation[0], annotation[1], value=label)
                    else:
                        line = 'delete {} in {} label {}'.format(annotation, filepath_in, label)
                        print(line)

                except:
                    print('exception')
                    pass

            for annotation in eafob.get_annotation_data_for_tier(ort_tier_names[1]):
                label = annotation[2]
                if label != '':
                    eafob_new.add_annotation(ort_tier_names[1], annotation[0], annotation[1], value=annotation[2])
                
            eafob_new.to_file(filepath_out)
    
def main(args):
       
    folder_in =args.input
    folder_out = args.output
    corrections_file = args.corrections
    deletes_file = args.deletes
    
    # DICT cambios que se aplicaran, par key/value = label_actual / label_correcta
    corrections_dict = {
        'FACIL' : 'F??CIL'
    }

    deletes = [':']
    
    if not corrections_file=='':
        corrections_dict = utils.parser_file_into_dict(corrections_file)
        
    if not corrections_file=='':
        deletes = utils.parser_file(deletes_file)
        
    print (corrections_dict)
    print (deletes)
    
    eaf_correction(folder_in, folder_out, corrections_dict, deletes)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Generate Result Output')
    parser.add_argument('--input', required=True, default='', type=str)
    parser.add_argument('--output', required=True, default='', type=str)
    parser.add_argument('--corrections', required=False, default='', type=str)
    parser.add_argument('--deletes', required=False, default='', type=str)
    arg = parser.parse_args()
    main(arg)


# python correct_eaf.py --input /home/temporal2/mvazquez/Challenge/utils_eaf/data/8ABR/eaf --output /home/temporal2/mvazquez/Challenge/utils_eaf/data/8ABR/eaf_ok --corrections corrections.txt --deletes deletes.txt
