import os
import argparse
import find_label_into_eaf
import utils


def main(args):
       
    folder_in =args.input
    folder_out =args.output
    label =args.label
    remove = args.rm_original
    
    print ('folder_in: {}'.format(folder_in))
    print ('folder_out: {}'.format(folder_out))
    print ('label: {}'.format(label))
    print ('remove: {}'.format(remove))
    
    utils.create_folder(folder_out)
    
    arr_detections, list_filenames = find_label_into_eaf.eaf_seach_annotation(folder_in, label)
    print(arr_detections)
    print('filenames: {}'.format(list_filenames))
    
    # Get same file_id
    
    for filename_idx in list_filenames:
        try:
            print('processing filename_idx: {} ....'.format(filename_idx))
            arr_detections_idx = arr_detections[arr_detections[:,0] == filename_idx]
            print (arr_detections_idx)
            
            filepath_in = os.path.join(folder_in, filename_idx)
            filepath_out = os.path.join(folder_out, filename_idx)
            
            number_detections = len(arr_detections_idx)
            print ('number_detections: {}'.format(number_detections))
            
            
            start = 0
            for idx, detection_idx in enumerate(arr_detections_idx):
                print('processing detection_idx: {} ....'.format(detection_idx))
                
                end = int(detection_idx[1])
                
                utils.segmentation_video(filepath_in, filepath_out, start, end, idx)
                utils.segmentation_eaf(filepath_in, filepath_out, start, end, idx)
                start = int(detection_idx[2])
                
            utils.segmentation_video(filepath_in, filepath_out, start, -1, idx+1)
            utils.segmentation_eaf(filepath_in, filepath_out, start, -1, idx+1)
            
            if remove:
                cmd = 'rm {}.eaf'.format(filepath_in)
                print (cmd)
                os.system(cmd)

                cmd = 'rm {}.mp4'.format(filepath_in)
                print (cmd)
                os.system(cmd)
        except:
            print ('Problem: {}'.format(filename_idx))


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Generate Result Output')
    parser.add_argument('--input', required=True, default='', type=str)
    parser.add_argument('--output', required=True, default='', type=str)
    parser.add_argument('--label', required=True, default='', type=str)
    parser.add_argument('--rm_original', action='store_true')
    arg = parser.parse_args()
    main(arg)


# Cut eaf and video in other folder -- keep original files
# python cut_eaf_and_video.py --input /home/temporal2/mvazquez/Challenge/utils_eaf/data/8ABR/cut --output /home/temporal2/mvazquez/Challenge/utils_eaf/data/8ABR/cut_out --label :

# Cut eaf and video in the same folder and remove original files
# python cut_eaf_and_video.py --input /home/temporal2/mvazquez/Challenge/utils_eaf/data/8ABR/cut --output /home/temporal2/mvazquez/Challenge/utils_eaf/data/8ABR/cut --label : --rm_original