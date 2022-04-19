import pympi
import os
import argparse
import numpy as np
import get_labels_eaf
import find_label_into_eaf
import utils


def calculate_range_interval_to_cut(all_anns, duration):
    size_min = duration + int(duration/2)

    intervals_without_signs = []
    for anns_idx in range(len(all_anns)-1):
        if all_anns[anns_idx+1][1] - all_anns[anns_idx][2] > size_min:
            interval_range = [all_anns[anns_idx][2], all_anns[anns_idx+1][1]]
            intervals_without_signs.append(interval_range)
    return intervals_without_signs


def calculate_interval_to_cut(intervals_without_signs, duration):

    print('select random between 0 and {}'.format(len(intervals_without_signs)-1))
    select_interval_random = np.random.randint(
        low=0, high=len(intervals_without_signs), size=1, dtype=int)[0]
    print('result: {}'.format(select_interval_random))
    print('select_interval_random: {}'.format(select_interval_random))

    interval_range = intervals_without_signs[select_interval_random]

    interval_to_search = (interval_range[1] - interval_range[0]) - duration
    if interval_to_search > 0:
        start_random = np.random.randint(
            low=0, high=interval_to_search, size=1, dtype=int)[0]
        start_calculated = interval_range[0]+start_random
        end_calculated = start_calculated + duration
        interval_out = [start_calculated, end_calculated]
        return interval_out

    return None


def main(args):

    folder_in = args.input
    folder_out = args.output
    duration = args.duration
    classes = args.classes
    repetitions = args.repetitions

    print('folder_in: {}'.format(folder_in))
    print('folder_out: {}'.format(folder_out))

    utils.create_folder(folder_out, reset=False)

    list_files = os.listdir(folder_in)
    list_labels = utils.parser_file(classes)

    for file_idx in list_files:
        if '.eaf' in file_idx:
            filepath_in = os.path.join(folder_in, file_idx.replace(".eaf", ""))
            filepath_out = os.path.join(
                folder_out, file_idx.replace(".eaf", ""))
            all_anns = utils.get_all_annotations(filepath_in, list_labels)
            print(all_anns)

            intervals_without_signs = calculate_range_interval_to_cut(
                all_anns, duration)

            print('intervals_without_signs: ')
            print(intervals_without_signs)

            print('filepath_in: {}'.format(filepath_in))

            if len(intervals_without_signs) < repetitions:
                repetitions_idx = len(intervals_without_signs)
            else:
                repetitions_idx  = repetitions

            if repetitions_idx > 0:
                for repetition_idx in range(repetitions_idx):
                    interval_out = calculate_interval_to_cut(
                        intervals_without_signs, duration)

                    print('interval_out')
                    print(interval_out)

                    if interval_out != None:

                        start = interval_out[0]
                        end = interval_out[1]

                        utils.segmentation_video(
                            filepath_in, filepath_out, start, end, repetition_idx)
                        utils.segmentation_eaf(
                            filepath_in, filepath_out, start, end, repetition_idx)
                    else:
                        print('INTERVAL OUT. DISCARD!!!!!!!!!!!!!!!')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Generate Result Output')
    parser.add_argument('--input', required=True, default='', type=str)
    parser.add_argument('--output', required=True, default='', type=str)
    parser.add_argument('--duration', required=True, default=5000, type=int)
    parser.add_argument('--classes', required=True, default='', type=str)
    parser.add_argument('--repetitions', required=False, default=2, type=int)
    arg = parser.parse_args()
    main(arg)


# python cut_track_vacios.py --input /home/temporal2/mvazquez/Challenge/utils_eaf/data/12ABR/ANOTADOS_TRACK2A --output /home/temporal2/mvazquez/Challenge/utils_eaf/data/12ABR/ANOTADOS_TRACK2_out_4000 --duration 4000 --classes /home/temporal2/mvazquez/Challenge/utils_eaf/data/track2.txt
