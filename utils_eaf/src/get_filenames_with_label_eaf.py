import os
import argparse
import find_label_into_eaf

def create_folder(folder):
    print ('create_folder: {}'.format(folder))    
    try:
        os.makedirs(folder)    
        print("Directory " , folder ,  " Created ")
    except FileExistsError:
        print("Directory " , folder ,  " already exists")
        
def parser_file(filepath):
    print ('parser_file')
    removes = []
    with open(filepath) as f:
        contents = f.readlines()
        try:
            for line in contents:
                removes.append(line.strip())
        except:
            pass
    return removes    
    
def write_list_filename(list_filenames, filepath):
    print ('write_list_filename: {}'.format(filepath))
    print ('list_filenames: {}'.format(list_filenames))
    
    with open(filepath, 'w') as file_handler:
        for item in list_filenames:
            file_handler.write("{}\n".format(item))
    
    
def main(args):
       
    folder_in =args.input
    folder_out = args.output
    label =args.label
    file_labels = args.file_labels
    
    create_folder(folder_out)
    
    list_labels = []
    if not label == '':
        print ('Single label')
        list_labels.append(label)
        pass
    elif not file_labels == '':
        print ('Multiple labels: {}'.format(file_labels))
        list_labels = parser_file(file_labels)
        pass
    else:
        raise Exception('error need add label o file_labels') 
    
    print ('list_labels')
    print (list_labels)
    
    for label_idx in list_labels:
       _, list_filenames = find_label_into_eaf.eaf_seach_annotation(folder_in, label_idx)
       filepath = os.path.join (folder_out, label_idx+'.txt')
       write_list_filename(list_filenames, filepath)
       
    


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Generate Result Output')
    parser.add_argument('--input', required=True, default='', type=str)
    parser.add_argument('--output', required=True, default='', type=str)
    parser.add_argument('--label', required=False, default='', type=str)
    parser.add_argument('--file_labels', required=False, default='', type=str)
    arg = parser.parse_args()
    main(arg)


# python get_filenames_with_label_eaf.py --input /home/temporal2/mvazquez/Challenge/utils_eaf/data/10ABR/ANOTADOS_TRACK2 --output /home/temporal2/mvazquez/Challenge/utils_eaf/data/10ABR/ANOTADOS_TRACK2_info --label CUIDAR
# python get_filenames_with_label_eaf.py --input /home/temporal2/mvazquez/Challenge/utils_eaf/data/10ABR/ANOTADOS_TRACK2 --output /home/temporal2/mvazquez/Challenge/utils_eaf/data/10ABR/ANOTADOS_TRACK2_info2 --file_labels /home/temporal2/mvazquez/Challenge/utils_eaf/data/track2_2.txt