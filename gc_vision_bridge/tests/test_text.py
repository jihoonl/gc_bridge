#!/usr/bin/env python

import json
import numpy
import sys
import cv2
import gc_vision_bridge
import os

def get_image_filepath():
    if len(sys.argv) < 2:
        print "Image file is not set. Use default 'newyork_rescaled.jpg'"
        imgname = 'newyork_rescaled.jpg'
    else:
        imgname = sys.argv[1]
    img_dir = os.environ["GC_VISION_TEST_IMAGE_DIR"]
    image_filepath = os.path.join(img_dir, imgname)

    return image_filepath

def print_texts(response):
    result = response['responses'][0]
    print json.dumps(result, indent=2, sort_keys=True)

def show_detection(image, response):
    result = response['responses'][0]

    if not 'textAnnotations' in result:
        print "No Text"
        return

    for f in result['textAnnotations']:
        box = [(v['x'], v['y']) for v in f['boundingPoly']['vertices']]
        pts = numpy.array(box, numpy.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(image, [pts], True, (0,255,0), thickness=2)


if __name__ == '__main__':
    print "Hello!"
    img_filepath = get_image_filepath()
    gcv_bridge = gc_vision_bridge.VisionBridge()
    print "Initialised"

    cv_image = cv2.imread(img_filepath)
    with open(img_filepath) as f:   
        image = f.read()
    features = gc_vision_bridge.create_feature_list('TEXT_DETECTION')
    
    result = gcv_bridge.request_raw(image, features) 

    print_texts(result)
    show_detection(cv_image, result)
    cv2.imshow('detected', cv_image)

    cv2.waitKey(0)                 # Waits forever for user to press any key
    cv2.destroyAllWindows()        # Closes displayed windows
