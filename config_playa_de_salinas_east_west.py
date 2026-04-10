# config file for IoT/Big Data project

#definition of regions:
#one entry of the dictionary is one livestream. It stores the url of the stream, the regions to zoom and identify objects separately, the video capture and the result file container and writer
STREAMS = {
    'playa-de-salinas-west': {
        'URL': 'https://webcams24.live/webcam/playa-de-salinas-west-webcam',
        'zooms': {'left': [0.5, 0.649, 0.5, 0.875], 'middle' :[0.651, 0.799, 0.525, 0.95], 'right' :[0.801, 1, 0.55, 1]}, 
        'cap': None,
        'result': {'file': None, 'write': None}
    },
    'playa-de-salinas-east': {
        'URL': 'https://webcams24.live/webcam/playa-de-salinas-east-webcam',
        'zooms': {'left': [0.0, 0.199, 0.55, 1], 'middle' :[0.201, 0.349, 0.505, 0.9], 'right' :[0.351, 0.5, 0.48, 0.78]}, 
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
SIZE = (1280,960) #None#(640, 480) #None 

#data is output either in SQL or CSV format. #set SQL to True for SQL format, and to False to CSV format
SQL = False 

#restart stream if an error occurs: in this case a new file is created but the data colleciton will continue. Otherwise it exits and no more data is collected.
loop_on_error = True

#parameters for zoom splitting, if zoom iss too wide or too tall -> to improve object detection
split_ratio_scale = 1.8
split_zooms_overlap_x = 0.075
split_zooms_overlap_y = 0.15
merge_dist_thresh = 5































"""
"https://www.youtube.com/live/8JCk5M_xrBs?si=mznENs30Y_VPM2V6"
"https://www.youtube.com/watch?v=Cp4RRAEgpeU"
"https://webcams24.live/webcam/egmond-aan-zee-holland-pompplein-webcam"
"https://webcams24.live/webcam/kabukich-shinjuku-japan-webcam"
"https://webcams24.live/webcam/sweet-soul-cafe-view-2-koh-samui-webcam"
"https://webcams24.live/webcam/playa-de-salinas-west-webcam"
"https://webcams24.live/webcam/playa-de-salinas-east-webcam"

REGIONS ={
    'Knokke': {'URL': 'https://webcams24.live/webcam/anemos-beach-club-knokke-heist-webcam', 'zoom':[0.18,0.95,0.45,0.85], 'cap': None, 'result': {'file': None, 'write': None}},
    'Salinas': {'URL': 'https://webcams24.live/webcam/playa-de-salinas-west-webcam', 'zoom':[0.2,0.95,0.5,0.95], 'cap': None, 'result': {'file': None, 'write': None}},
    'Zeeland': {'URL': 'https://webcams24.live/webcam/renesse-aan-zee-beach-zeeland-webcam', 'zoom':[0.2,0.8,0.35,0.8], 'cap': None, 'result': {'file': None, 'write': None}}
}

'Begavna': {'URL': 'https://webcams24.live/webcam/san-silvestro-church-square-begavna-webcam', 'zoom':[0.15,0.7,0.55,0.99], 'cap': None, 'result': {'file': None, 'write': None}}
"""