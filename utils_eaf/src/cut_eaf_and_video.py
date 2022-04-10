import pympi
import os
import argparse
import numpy as np
import find_label_into_eaf

def create_folder(folder):
    print ('create_folder: {}'.format(folder))    
    try:
        os.makedirs(folder)    
        print("Directory " , folder ,  " Created ")
    except FileExistsError:
        print("Directory " , folder ,  " already exists")

def segmentation_video(filepath_in, filepath_out, start, end, idx):
    
    video_path='{}.mp4'.format(filepath_in)
    out_video_path='{}_{}.mp4'.format(filepath_out, idx)
    
    start = start * 1e-3
    end = end * 1e-3
    dur = end - start
    
    if dur>0:
        cmd = 'ffmpeg -i {} -ss {} -t {} {} -loglevel quiet'.format(video_path,  start, dur, out_video_path)
    else:
        cmd = 'ffmpeg -i {} -ss {} {} -loglevel quiet'.format(video_path,  start, out_video_path)
    print (cmd)
    
    os.system(cmd)
    
def segmentation_eaf(filepath_in, filepath_out, start, end, idx):
    
    eaf_path='{}.eaf'.format(filepath_in)
    out_eaf_path='{}_{}.eaf'.format(filepath_out, idx)
    
    eafob = pympi.Elan.Eaf(eaf_path)
    eafob_new = pympi.Elan.Eaf(eaf_path)
    eafob_new.remove_linked_files(mimetype='video/mp4')
    
    relpath = './{}_{}.mp4'.format(os.path.basename(filepath_in), idx)
    eafob_new.add_linked_file('{}.mp4'.format(relpath),relpath=relpath, mimetype='video/mp4')
    
    ort_tier_names=list(eafob.get_tier_names())
    
    for tier_idx in ort_tier_names:

        eafob_new.remove_tier(tier_idx,clean=True)
        eafob_new.add_tier(tier_idx)
        
        for annotation in eafob.get_annotation_data_for_tier(tier_idx):
            
            if (annotation[0]>start):
                if (annotation[0]<end or end<0):
                    eafob_new.add_annotation(tier_idx, annotation[0] - start, annotation[1] - start, value=annotation[2])
            
    eafob_new.to_file(out_eaf_path)

    
def main(args):
       
    folder_in =args.input
    folder_out =args.output
    label =args.label
    remove = args.rm_original
    
    print ('folder_in: {}'.format(folder_in))
    print ('folder_out: {}'.format(folder_out))
    print ('label: {}'.format(label))
    print ('remove: {}'.format(remove))
    
    create_folder(folder_out)
    
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
                
                segmentation_video(filepath_in, filepath_out, start, end, idx)
                segmentation_eaf(filepath_in, filepath_out, start, end, idx)
                start = int(detection_idx[2])
                
            segmentation_video(filepath_in, filepath_out, start, -1, idx+1)
            segmentation_eaf(filepath_in, filepath_out, start, -1, idx+1)
            
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