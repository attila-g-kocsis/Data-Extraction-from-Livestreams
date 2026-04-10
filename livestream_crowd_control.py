############################## LIBRARY IMPORTS ##############################

import sys, subprocess
from datetime import datetime
from zoneinfo import ZoneInfo
import numpy as np
import math
import cv2
from ultralytics import YOLO
import sqlite3, csv 


############################## IMPORT PARAMETERS ##############################

from config_basilica_of_saint_francis import *
#from config_playa_de_salinas_east import *
#from config_playa_de_salinas_east_west import *


############################## HELPER FUNCTIONS ##############################

#csv file initializer
def init_csv(filename):
    csv_file = open(filename, "a", newline="")
    writer = csv.writer(csv_file)
    # header
    key=list(STREAMS.keys())[0]
    STREAMS[key]['zooms'].keys()
    zoom_names=list(STREAMS[key]['zooms'].keys())
     
    writer.writerow(["timestamp"] +["Num. "+item+"s in zoom "+zoom_name for zoom_name in zoom_names for item in classes_to_detect])
    return csv_file, writer

#sql file initializer
def init_sql(filename):
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    # header    
    key=list(STREAMS.keys())[0]
    STREAMS[key]['zooms'].keys()
    zoom_names=list(STREAMS[key]['zooms'].keys())    
    columns_def = "timestamp TEXT,\n    " + ",\n    ".join([f"Num_{item}s_in_zoom_{zoom_name} INTEGER" for zoom_name in zoom_names for item in classes_to_detect])

    sql_string = f"""
    CREATE TABLE IF NOT EXISTS counts (
        {columns_def}
    )
    """    
    cur.execute(sql_string)
    return conn, cur

#url getter
def get_stream_url(url: str) -> str:
    cmd = ["yt-dlp", "-g", "--no-warnings", url]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    # return first valid stream (prefer m3u8)
    for line in result.stdout.splitlines():
        if "m3u8" in line or line.startswith("http"):
            return line.strip()

    raise RuntimeError("No stream found")

#Histogram Equalization / CLAHE
def improve_contrast(frame):
    yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    yuv[:,:,0] = clahe.apply(yuv[:,:,0])
    return cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)

#Brightness / Gamma adjustment
def improve_brightness(frame):
    gamma = 1.5  # >1 = brighter
    invGamma = 1.0 / gamma
    gamma_table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(256)]).astype("uint8")    
    return cv2.LUT(frame, gamma_table)

#object detection in aspecified window of a frame
def detect_objects_in_window(frame, x0, x1, y0, y1, model, text_size=2, text_shift=-80, color=(0,255,0)):
        
    #YOLO 
    results = model(frame[y0:y1,x0:x1,:], verbose=False)            
    
    #filtering predictions for given objects to detect
    filtered_predictions = {item:[] for item in classes_to_detect}

    for pred in results[0].boxes:  # results[0].boxes contains all boxes
        class_name = results[0].names[int(pred.cls)]

        if class_name in classes_to_detect:
            filtered_predictions[class_name].append(pred)
    
    #showing given region object to detect within
    cv2.rectangle(frame, (x0, y0), (x1, y1), color, 1)   

    #count and indicate object occurences
    object_occurence = np.zeros(len(classes_to_detect), dtype=int)
    object_centers = [None]*len(classes_to_detect)
    object_center = None

    for i,class_name in enumerate(classes_to_detect):
        object_occurence[i]=len(filtered_predictions[class_name])
        cv2.putText(frame, f"{class_name}s: {object_occurence[i]}", (int((x0+x1)/2+text_shift), int(y0-(i+1)*(9+text_size))), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, text_size) #OBJECT_COLORS[i], 1)              

    #tag detected objects
    for i,key in enumerate(filtered_predictions.keys()):

        for pred in filtered_predictions[key]:
            xo0, yo0, xo1, yo1 = map(int, pred.xyxy[0])
            object_center = (int((xo0+xo1)/2.0+x0), int((yo0+yo1)/2.0+y0))
            cv2.circle(frame, object_center, 2, color, -1) 
            if object_centers[i]: 
                object_centers[i].append(np.array(object_center))
            else:
                object_centers[i] = [np.array(object_center)]

    return np.array(list(map(int, object_occurence))), object_centers

#merge detections if a zoom was split in 2
def merge_detections(centers_1, centers_2, frame, x_text, y_text, text_size=2, text_shift=-80, color=(0,255,0)):

    num_classes_to_detect = len(centers_1)
    a_counts = [None]*num_classes_to_detect

    for k in range(num_classes_to_detect):
        center_1 = centers_1[k]
        center_2 = centers_2[k]

        if center_1 is None:
            center_1 = []
        if center_2 is None:
            center_2 = []

        merged = list(center_1)

        for c2 in center_2:
            duplicate = False
            for c1 in merged:
                dist = math.hypot(c1[0] - c2[0], c1[1] - c2[1])
                if dist < merge_dist_thresh:
                    duplicate = True
                    break

            if not duplicate:
                merged.append(c2)
                
        a_counts[k] = len(merged)
        
        cv2.putText(frame, f"Total {classes_to_detect[k]}s: {len(merged)}", (int(x_text+text_shift), int(y_text-(k+1)*(9+text_size))), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, text_size)
    
    return a_counts 


############################## MANIN FUNCTION ##############################

def main():
    try:
        print("Loading YOLO-model ...")
        model = YOLO(MODEL_PATH)

        #make unit file stamp from current time
        timestamp_0 = datetime.now(ZoneInfo("Europe/Brussels")).isoformat().split('.')[0].replace(':','-')

        for key, value in STREAMS.items():

            print("Getting URL-stream and capturing video for "+key+" ...")
            STREAMS[key]['cap'] = cv2.VideoCapture(get_stream_url(value['URL']), cv2.CAP_FFMPEG) 

            if SQL:
                STREAMS[key]['result']['file'], STREAMS[key]['result']['writer'] = init_sql(timestamp_0+'_'+key+'_max.db')
            else:
                STREAMS[key]['result']['file'], STREAMS[key]['result']['writer'] = init_csv(timestamp_0+'_'+key+'_max.csv')            

        num_zooms = len(list(value['zooms'].keys()))
        num_classes_to_detect = len(classes_to_detect)        

        #initializations for averages over seconds        
        current_second = None
        all_counts = np.zeros((num_zooms, num_classes_to_detect))                   
        max_counts = np.zeros((num_zooms, num_classes_to_detect))             

        while True:
            frames = []

            for key, value in STREAMS.items():
                ret, frame = value['cap'].read()

                if not ret:
                    STREAMS[key]['cap'].release()
                    STREAMS[key]['cap'] = cv2.VideoCapture(get_stream_url(value['URL']), cv2.CAP_FFMPEG) #try to reconnect if streaming is lost
                    continue               

                else:
                    if SIZE is not None:
                        frame = cv2.resize(frame, SIZE)
                    #region to detect object in the frame (nummpy array slice)
                    frame_width=frame.shape[1]  #first index is along height, from the top
                    frame_height=frame.shape[0] #null  index is the width,    from the left                     

                    #timestamp
                    timestamp = datetime.now(ZoneInfo("Europe/Brussels"))                    
                    #average over a second
                    second_key = timestamp.replace(microsecond=0)

                    for i,zoom_key in enumerate(value['zooms'].keys()):

                        xa0 = int(frame_width*value['zooms'][zoom_key][0]) 
                        xa1 = int(frame_width*value['zooms'][zoom_key][1])
                        ya0 = int(frame_height*value['zooms'][zoom_key][2]) 
                        ya1 = int(frame_height*value['zooms'][zoom_key][3])

                        w = xa1-xa0
                        h = ya1-ya0
                        too_wide = w > split_ratio_scale*h
                        too_tall = h > split_ratio_scale*w

                        # YOLO inference   

                        #split window in 2 if zoomed region is too wide
                        if too_wide:                         
                            #split window in 2 horizontally:
                            _, centers_1  = detect_objects_in_window(frame, xa0, int(xa0+w*(0.5+split_zooms_overlap_x/2)), ya0, ya1, model, text_size=1, text_shift=-w/4, color=ZOOM_COLORS[i])
                            _, centers_2  = detect_objects_in_window(frame, int(xa0+w*(0.5-split_zooms_overlap_x/2)), xa1, ya0, ya1, model, text_size=1, text_shift= w/4-80, color=ZOOM_COLORS[i])
                        
                            all_counts[i] = merge_detections(centers_1, centers_2, frame, (xa0+xa1)/2, ya0, text_size=1, text_shift=-50, color=ZOOM_COLORS[i])

                        #split window in 2 if zoomed region is too tall
                        elif too_tall:
                            #split window in 2 vertically:
                            _, centers_1  = detect_objects_in_window(frame, xa0, xa1, ya0, int(ya0+h*(0.5+split_zooms_overlap_y/2)), model, text_size=1, text_shift=-90, color=ZOOM_COLORS[i])
                            _, centers_2  = detect_objects_in_window(frame, xa0, xa1, int(ya0+h*(0.5-split_zooms_overlap_y/2)), ya1, model, text_size=1, text_shift=90, color=ZOOM_COLORS[i])
                        
                            all_counts[i] = merge_detections(centers_1, centers_2, frame, w/2, h/2, text_size=2, text_shift=-55, color= ZOOM_COLORS[i])

                        else:             
                            all_counts[i], _ = detect_objects_in_window(frame, xa0, xa1, ya0, ya1, model, text_size=2, color=ZOOM_COLORS[i])   

                        # initialize
                        if current_second is None:
                            current_second = second_key

                    #if second changed, then compute average
                    if second_key != current_second:
                        max_counts = np.maximum(max_counts,all_counts)

                        if SQL:
                            sql_string = f"INSERT INTO counts VALUES ({'?, '*(num_zooms*num_classes_to_detect)} ?)"               
 
                            STREAMS[key]['result']['writer'].execute(sql_string, tuple([timestamp.isoformat().split('.')[0]] + [x for sub in max_counts for x in sub]))

                            STREAMS[key]['result']['file'].commit()              
                        else:  
                            STREAMS[key]['result']['writer'].writerow([timestamp.isoformat().split('.')[0]] + [x for sub in max_counts for x in sub])                                                               
                            STREAMS[key]['result']['file'].flush()   
                        #reset for new second
                        current_second = second_key
                        max_counts = np.zeros((num_zooms, num_classes_to_detect))  

                frames.append(frame)
         
            grid = cv2.hconcat(frames)
            cv2.imshow("Crowd controll with multi-region YOLO", grid)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        for key, value in STREAMS.items():
            STREAMS[key]['cap'].release()
            if SQL:
                STREAMS[key]['result']['writer'].close()            
            STREAMS[key]['result']['file'].close()

        cv2.destroyAllWindows()

    except Exception as e:
        print(f"Error: {e}")
        if loop_on_error:
            main()
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()