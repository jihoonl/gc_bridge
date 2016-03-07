#!/usr/bin/env python

import json
import sys
import cv2
import gc_vision_bridge
import os

def get_image_filepath():
    imgfile = 'newyork_rescaled.jpg'
    if len(sys.argv) < 2:
        print "Image file is not set. Use default '%s'"%imgfile
        imgname = imgfile
    else:
        imgname = sys.argv[1]
    img_dir = os.environ["GC_VISION_TEST_IMAGE_DIR"]
    image_filepath = os.path.join(img_dir, imgname)

    return image_filepath

def print_labels(response):
    result = response['responses'][0]
    #print json.dumps(result, indent=2, sort_keys=True)

    if 'landmarkAnnotations' not in result:
        print "No landmark"
        return

    print("%-20s\t\t%-20s\t%-20s"%("Description","Score","Location(LatLng)"))
    print("================================================================")
    for r in result['landmarkAnnotations']:
        if not 'description' in r:
            continue
        if r['locations']: 
            lat = r['locations'][0]['latLng']['latitude']
            lo = r['locations'][0]['latLng']['longitude']
            print("%-20s\t\t%-20s\t%-10s,%-10s"%(r['description'], r['score'],lat, lo))
        else:
            print("%-20s\t\t%-20s\t%-10s,%-10s"%(r['description'], r['score']))

if __name__ == '__main__':
    print "Hello!"
    img_filepath = get_image_filepath()
    gcv_bridge = gc_vision_bridge.VisionBridge()
    print "Initialised"

    cv_image = cv2.imread(img_filepath)
    with open(img_filepath) as f:   
        image = f.read()
    features = gc_vision_bridge.create_feature_list('LANDMARK_DETECTION')
    
    cv2.imshow('original', cv_image)
    result = gcv_bridge.request_raw(image, features) 

    print_labels(result)

    cv2.waitKey(0)                 # Waits forever for user to press any key
    cv2.destroyAllWindows()        # Closes displayed windows
