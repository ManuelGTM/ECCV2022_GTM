from operator import truediv
import pympi
import numpy as np
import utils

class Utils_Eaf():
    def __init__(self, pathfile):
        self.pathfile = pathfile
        self.eafob = pympi.Elan.Eaf(pathfile)
        self.ort_tier_names=list(self.eafob.get_tier_names()):
        pass
    
    def reset(self, relpath):
        self.eafob.remove_linked_files(mimetype='video/mp4')
        self.eafob.add_linked_file('{}.mp4'.format(relpath),relpath=relpath, mimetype='video/mp4')
        
        for tier_idx in self.ort_tier_names:
            self.eafob.remove_tier(tier_idx,clean=True)
            
    def get_name_tier_main(self):
        return self.ort_tier_names[0]
    
    def get_name_tier_variations(self):
        return self.ort_tier_names[1]
            
    def add_tier(self, tier_name):
        self.eafob.add_tier(tier_name)
        
    def insert_annotation(self, tier_name, start, end, label):
        self.eafob.add_annotation(tier_name, start, end, value=label)
        
    def is_available_annotation(self, tier_name, time):
        
        print (self.eafob.get_annotation_data_at_time(self.get_name_tier_main, time))
        
        return True
        
    def save(self, out_eaf_path):
        self.eafob.to_file(out_eaf_path)