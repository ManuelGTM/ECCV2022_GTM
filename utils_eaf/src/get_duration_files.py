from numpy import append
import pympi
import os
import argparse
import json
import utils
import cv2
import datetime


def get_duration_video(filepath_vid_in):
    video = cv2.VideoCapture(filepath_vid_in)

    # count the number of frames
    frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    
    # calculate dusration of the video
    seconds = int(frames / fps)
    video_time = str(datetime.timedelta(seconds=seconds))
    print("duration in seconds:", seconds)
    print("video time:", video_time)

    
    return video_time


def get_number_annotations_track(list_labels, track):
    counter = 0
    for label_idx in list(list_labels.keys()):
       if label_idx in track:
           counter = counter + 1
    return counter

def get_duration_annotations_track(list_labels, track):
    duration = 0
    for label_idx in list(list_labels.keys()):
       if label_idx in track:
           duration = duration + list_labels[label_idx]
    return duration
    
        
def eaf_get_list_anns(path_folder_eaf, asterisk, spaces, track1, track2):
    lst_files = os.listdir(path_folder_eaf)
    info_annotations = {}
    list_filenames=[]
    list_labels_all=[]
    
    info_annotations['labels'] = []
    info_annotations['filenames'] = []
    
    for elan_file in lst_files:
        if '.eaf' in elan_file:
            filepath_in = os.path.join(path_folder_eaf, elan_file)
            filepath_vid_in = os.path.join(path_folder_eaf, elan_file.replace('.eaf','.mp4'))

            eafob = pympi.Elan.Eaf(filepath_in)
            ort_tier_names=list(eafob.get_tier_names())
            
            filename = elan_file.replace('.eaf','')
            list_filenames.append(filename)
            list_labels = {}
            
            
            for annotation in eafob.get_annotation_data_for_tier(ort_tier_names[0]):
                print (annotation)
                try:
                    label = annotation[2]
                    if spaces:
                        label = label.replace(' ','')
                    if asterisk:
                        label = label.replace('*','')
                    
                    print(label)
                    
                    
                    if label not in list_labels_all:
                        list_labels_all.append(label)
                        
                    list_labels[label] = annotation[1] - annotation[0]

                except:
                    print('exception')
                    pass
        
            info_annotations[filename] = {
                'track1' : get_number_annotations_track(list_labels, track1),
                'track1_ms' : get_duration_annotations_track(list_labels, track1),
                'track2' : get_number_annotations_track(list_labels, track2),
                'track2_ms' : get_duration_annotations_track(list_labels, track2),
                'duration' : get_duration_video(filepath_vid_in),
                'labels' : list_labels
            }
        
        
    info_annotations['labels'] = list_labels_all
    info_annotations['filenames'] = list_filenames
        
    return info_annotations
    
def main(args):
       
    folder_in =args.input
    file_out =args.output
    rm_asterisk =args.rm_asterisk
    rm_spaces =args.rm_spaces
    track1_file =args.track1
    track2_file =args.track2
    
    
    track1 = utils.parser_file(track1_file)
    track2 = utils.parser_file(track2_file)
    
    # utils.create_folder(file_out, reset=True)
    
    print ('return Data annotations')
    dict_eaf_info = eaf_get_list_anns(folder_in, rm_asterisk, rm_spaces, track1, track2)
    
    with open(file_out, "w") as outfile:
        json.dump(dict_eaf_info, outfile)
    
    print (dict_eaf_info)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Generate Result Output')
    parser.add_argument('--input', required=True, default='', type=str)
    parser.add_argument('--output', required=True, default='', type=str)
    parser.add_argument('--track1', required=True, default='', type=str)
    parser.add_argument('--track2', required=True, default='', type=str)
    parser.add_argument('--rm_asterisk', action='store_true')
    parser.add_argument('--rm_spaces', action='store_true')
    arg = parser.parse_args()
    main(arg)


# python get_duration_files.py --input /home/temporal2/mvazquez/Challenge/utils_eaf/data/9ABR/ANOTADOS_TRACK1_cut --output /home/temporal2/mvazquez/Challenge/utils_eaf/data/18ABR/INFO/ANOTACION_MARUXA --track1 /home/temporal2/mvazquez/Challenge/utils_eaf/data/track1.txt --track2 /home/temporal2/mvazquez/Challenge/utils_eaf/data/track2.txt --rm_asterisk --rm_spaces
