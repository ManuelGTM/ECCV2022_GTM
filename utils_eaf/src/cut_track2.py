import pympi
import os
import argparse
import numpy as np
import get_labels_eaf
import find_label_into_eaf
import utils
    
    
# def calculate_interval_to_cut(start, end, duration):
    
#     start_int = int(start)
#     end_int = int(end)
#     duration_int = int(duration)
    
#     duration_sign = end_int - start_int
#     duration_left = duration_int - duration_sign
    
#     if duration_left > start_int :
#         duration_left = start_int
#     start_random = np.random.randint(low=0, high=duration_left, size=1, dtype=int)[0]
    
#     start_calculated = start_int-start_random
#     end_calculated = start_calculated + duration_int
    
#     return start_calculated, end_calculated


def calculate_range_interval_to_cut(annotation, all_anns, duration):
    dur_inf = annotation[2]-duration
    dur_sup = annotation[1]+duration
    interval_range = [dur_inf, dur_sup]
    
    #print('interval_range: {} '.format(interval_range))
    
    # filter by same class
    anns_filter_sameclass = all_anns[all_anns[:,0] == annotation[0]]
    
    if anns_filter_sameclass.shape[0] > 1:
        idx = -1
        for anns_idx in range(len(anns_filter_sameclass)):
            if (anns_filter_sameclass[anns_idx]==annotation).all():
                idx = anns_idx
        try:
            distance_inf = anns_filter_sameclass[idx][1] - anns_filter_sameclass[idx-1][2]
            #print ('distance_inf: {}'.format(distance_inf))
            if distance_inf>0:
                dur_inf2 = anns_filter_sameclass[idx][1]-distance_inf
                if dur_inf2 > dur_inf:
                    dur_inf = dur_inf2
        except:
            print ('exception')
            
        try:
            distance_sup = anns_filter_sameclass[idx+1][1] - anns_filter_sameclass[idx][2]
            #print ('distance_sup: {}'.format(distance_sup))
            if distance_sup>0:
                dur_sup2 = anns_filter_sameclass[idx][2]+distance_sup
                if dur_sup2 < dur_sup:
                    dur_sup = dur_sup2
        except:
            print ('exception')
            
    interval_range = [dur_inf, dur_sup]
    #print('range check class id: {} '.format(interval_range))
            
    anns_filter = all_anns[(all_anns[:,2] >= dur_inf) & (all_anns[:,1] <= dur_sup)]
    #print('anns_filter: {} '.format(anns_filter))
    if (len(anns_filter) > 0):
        if anns_filter[0][1] < dur_inf:
            dur_inf = anns_filter[0][2]
            #print ('cut dur_inf: {}'.format(dur_inf))
            
        if anns_filter[-1][2] > dur_sup:
            dur_sup = anns_filter[-1][1]
            #print ('cut dur_inf: {}'.format(dur_sup))

    interval_range = [dur_inf, dur_sup]
    anns_filter_result = all_anns[(all_anns[:,2] >= dur_inf) & (all_anns[:,1] <= dur_sup)]
    return interval_range, anns_filter_result

def calculate_interval_to_cut(interval_range, interval_anns, duration):
    interval_to_search = ((interval_range[1]) - (interval_range[0])) - duration
    if interval_to_search > 0:
        
        check_interva_out = False
        while (check_interva_out == False):
            start_random = np.random.randint(low=0, high=interval_to_search, size=1, dtype=int)[0]
            start_calculated = interval_range[0]+start_random
            end_calculated = start_calculated + duration
            interval_out = [start_calculated, end_calculated]
            
            check_interva_out = check_interval_ok(interval_out, interval_anns)
            
        return interval_out
    else:
        return None
    
def check_interval_ok(interval_range, interval_anns):
    anns_filter_result = interval_anns[(interval_anns[:,2] >= interval_range[0]) & (interval_anns[:,1] <= interval_range[1])]
    if anns_filter_result[0][1] < interval_range[0]:
        return False
    if anns_filter_result[-1][2] > interval_range[1]:
        return False
    return True
        
        
        
def main(args):
       
    folder_in =args.input
    folder_out =args.output
    duration =args.duration
    classes=args.classes
    
    print ('folder_in: {}'.format(folder_in))
    print ('folder_out: {}'.format(folder_out))
    
    utils.create_folder(folder_out, reset=False)  
    
    list_files = os.listdir(folder_in)
    # list_labels = get_labels_eaf.eaf_get_list_anns(folder_in)
    
    list_labels = utils.parser_file(classes)
    
    idx = 0
    for file_idx in list_files:
        if '.eaf' in file_idx:
            filepath_in = os.path.join(folder_in, file_idx.replace(".eaf",""))
            filepath_out = os.path.join(folder_out, file_idx.replace(".eaf",""))
            all_anns = utils.get_all_annotations(filepath_in, list_labels)
            print (all_anns)
            
            print ('filepath_in: {}'.format(filepath_in))
            
            for ann_idx in all_anns:
                print ('IDX: {}'.format(idx))
                
                print ('ann_idx: {}'.format(ann_idx))
                interval_range, interval_anns_all = calculate_range_interval_to_cut(ann_idx, all_anns, duration)
                
                print ('INTERVAL_RANGE: {}'.format(interval_range))
                
                interval_out = calculate_interval_to_cut(interval_range, interval_anns_all, duration)
                
                print ('INTERVAL_OUT: {}'.format(interval_out))
                
                if interval_out != None:
                    print ('INTERVAL_OUT: {}'.format(interval_out))
                    start = interval_out[0]
                    end = interval_out[1]
                    idx = idx +1 
                    
                    filepath_out_with_class = os.path.join(folder_out, "["+str(ann_idx[0])+"]-"+file_idx.replace(".eaf",""))
                    
                    utils.segmentation_video(filepath_in, filepath_out_with_class, start, end, idx)
                    utils.segmentation_eaf(filepath_in, filepath_out_with_class, start, end, idx)
                else:
                    print ('INTERVAL OUT. DISCARD!!!!!!!!!!!!!!!')
                    
    print ('list_labels')
    for idx in range (len(list_labels)):
        print ('{} : {}'.format(idx, list_labels[idx]))
        


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Generate Result Output')
    parser.add_argument('--input', required=True, default='', type=str)
    parser.add_argument('--output', required=True, default='', type=str)
    parser.add_argument('--duration', required=True, default=5000, type=int)
    parser.add_argument('--classes', required=True, default='', type=str)  
    arg = parser.parse_args()
    main(arg)



# python cut_track2.py --input /home/temporal2/mvazquez/Challenge/utils_eaf/data/12ABR/ANOTADOS_TRACK2A --output /home/temporal2/mvazquez/Challenge/utils_eaf/data/12ABR/ANOTADOS_TRACK2_out_4000 --duration 4000 --classes /home/temporal2/mvazquez/Challenge/utils_eaf/data/track2.txt