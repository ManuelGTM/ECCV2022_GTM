import numpy as np

def extract_performances(data_gt, data_eval, threshold_iou):
    tp = fp = fn = 0
    if (data_gt.shape[0] == 0 and data_eval.shape[0] == 0):
        return tp, fp, fn
            
    if (data_gt.shape[0] == 0):
        fp = data_eval.shape[0]
        return tp, fp, fn

    if (data_eval.shape[0] == 0):
        fn = data_gt.shape[0]
        return tp, fp, fn
    
    data_eval_filtered = filter_overlap_interval(data_eval)
        
    for gt_idx in data_gt:
        class_id = gt_idx[0]
        data_gt_idx = np.delete(gt_idx, 0)            
        detections = 0
        
        data_eval_id = data_eval_filtered[data_eval_filtered[:,0]==class_id]
        for eval_idx in data_eval_id:
            data_eval_idx = np.delete(eval_idx, 0)
            if (get_temporal_iou_1d(data_eval_idx, data_gt_idx) >= threshold_iou):
                detections = detections + 1
        if detections > 0:
            tp = tp + 1
        
    fn = data_gt.shape[0] - tp
    fp = data_eval.shape[0] - tp

    return tp, fp, fn
    
    
def calculate_metrics(tp, fp, fn):
    try:
        precision = tp / (tp + fp)
    except:
        precision = 0
            
    try:
        recall = tp / (tp + fn)
    except:
        recall = 0
            
    try:
        f1 = (2 * (precision * recall)) / (precision + recall)
    except:
        f1 = 0
        
    return precision, recall, f1

def get_temporal_iou_1d(v1, v2):
    earliest_start = min(v1[0],v2[0])
    latest_start = max(v1[0],v2[0])
    earliest_end = min(v1[1],v2[1])
    latest_end = max(v1[1],v2[1]) 
    iou = (earliest_end - latest_start) / (latest_end - earliest_start)
    return 0 if iou < 0 else iou

def filter_overlap_interval(data):
    if data.shape[0] > 1:
        data_out = np.copy(data)
        data_true = np.array([ data[idx][0]!=data[idx+1][0] or data[idx][2]<data[idx+1][1] for idx in range(data.shape[0]-1)])
        data_true = np.append(data_true, True)
        return data_out[data_true]
    return data