# config file for IoT/Big Data project

#definition of regions:
#one entry of the dictionary is one livestream. It stores the url of the stream, the regions to zoom and identify objects separately, the video capture and the result file container and writer
STREAMS = {
    'basilica-of-saint-francis': {
        'URL': 'https://webcams24.live/webcam/basilica-of-saint-francis-of-assisi-webcam',
        'zooms': {'top': [0.32, 0.62, 0.7, 0.799], 'middle' :[0.277, 0.637, 0.801, 0.899], 'bottom' :[0.225, 0.65, 0.901, 0.999]},  #add more entries for more zoom regions        
        'cap': None,
        'result': {'file': None, 'write': None}
    },
}

#YOLO model path
MODEL_PATH = "yolo11n.pt"

#specify colors of the box visualization of zoomed regions where objects are detected
ZOOM_COLORS = ((255,255,0),  (0,0,255), (0,255,0), (255,0,0),  (255,0,255), (0,255,255), )

#add the object types to be identified. Multiple objects can be added, such as 'person', 'bicycle', 'dog', 'bagpack', "handbag", "cell phone"
classes_to_detect = ('person', ) 

#set size if you want multi-stream, or if you want reduced view
SIZE = None #(640, 480) 

#data is output either in SQL or CSV format. #set SQL to True for SQL format, and to False to CSV format
SQL = False #True

#restart stream if an error occurs: in this case a new file is created but the data colleciton will continue. Otherwise it exits and no more data is collected.
loop_on_error = True

#parameters for zoom splitting, if zoom iss too wide or too tall -> to improve object detection
split_ratio_scale = 1.8
split_zooms_overlap_x = 0.075
split_zooms_overlap_y = 0.15
merge_dist_thresh = 5