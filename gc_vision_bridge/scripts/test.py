#!/usr/bin/env python

import sys
import cv2
import gc_vision_bridge
import os

def get_credentials_filepath(): 
    return os.environ["GC_VISION_SECRET"]

def get_image_filepath():
    if len(sys.argv) < 2:
        print "Image file is not set. Use default 'newyork.jpg'"
        imgname = 'newyork_rescaled.jpg'
    else:
        imgname = sys.argv[1]
    img_dir = os.environ["GC_VISION_TEST_IMAGE_DIR"]
    image_filepath = os.path.join(img_dir, imgname)

    return image_filepath


def generate_default_features():
    return [ {"type":"LABEL_DETECTION",
              "maxResults": 10
             },
             {
              "type":"TEXT_DETECTION",
              "maxResults": 10
             },
             {
 
            "type":"FACE_DETECTION",
              "maxResults": 20
             }]

if __name__ == '__main__':
    print "Hello!"
    secret = get_credentials_filepath()
    img_filepath = get_image_filepath()
    gcv_bridge = gc_vision_bridge.Bridge(secret)
    print "Initialised"

    cv_image = cv2.imread(img_filepath)
    with open(img_filepath) as f:   
        image = f.read()
    features = generate_default_features()
    
    cv2.imshow('original', cv_image)
    result = gcv_bridge.request_raw(image, features) 
    print(str(result))
    cv2.waitKey(0)                 # Waits forever for user to press any key
    cv2.destroyAllWindows()        # Closes displayed windows
