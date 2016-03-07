#!/usr/bin/env python

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

def print_labels(response):
    result = response['responses'][0]['labelAnnotations']

    print(" %-20s\t\t%-20s"%("Label","Score"))
    print("=====================================")
    for r in result:
        print("%-20s\t\t%-20s"%(r['description'], r['score']))

if __name__ == '__main__':
    print "Hello!"
    img_filepath = get_image_filepath()
    gcv_bridge = gc_vision_bridge.VisionBridge()
    print "Initialised"

    cv_image = cv2.imread(img_filepath)
    with open(img_filepath) as f:   
        image = f.read()
    features = gc_vision_bridge.create_feature_list('LABEL_DETECTION')
    
    cv2.imshow('original', cv_image)
    result = gcv_bridge.request_raw(image, features) 

    print_labels(result)

    cv2.waitKey(0)                 # Waits forever for user to press any key
    cv2.destroyAllWindows()        # Closes displayed windows
