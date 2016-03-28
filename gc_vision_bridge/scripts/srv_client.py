#!/usr/bin/env python

import json
import sys
import os
import cv2
import rospy
import gc_vision_bridge
import gc_msgs.srv as gc_srvs
import sensor_msgs.msg as sensor_msgs
import numpy
from cv_bridge import CvBridge


def get_image():
    imgfile = 'royalmo.jpg'
    if len(sys.argv) < 2:
        print "Image file is not set. Use default '%s'"%imgfile
        imgname = imgfile
    else:
        imgname = sys.argv[1]
    img_dir = os.environ["GC_VISION_TEST_IMAGE_DIR"]
    image_filepath = os.path.join(img_dir, imgname)
    cv_image = cv2.imread(image_filepath)

    bridge = CvBridge()
    image_message = bridge.cv2_to_imgmsg(cv_image, encoding="bgr8")
    return image_message, cv_image

def get_emos(f):
    emos = {k:v for k, v in f.items() if k.endswith('Likelihood')}
    emos = {k:v for k, v in emos.items() if v != 'VERY_UNLIKELY'}
    return emos

def draw_emos(image, f, pos):
    emos = get_emos(f)
    if emos:
        for k,v in emos.items():
            t = "%s : %s"%(k,v)
            x = pos[0]
            y = pos[1]
            cv2.putText(image, t, (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

def show_detection(image, response):
    
    resp = eval(response)
    result = resp['responses'][0]

    if not 'faceAnnotations' in result:
        print "No Face"
        return

    for f in result['faceAnnotations']:
        box = [(v['x'], v['y']) for v in f['fdBoundingPoly']['vertices']]
        pts = numpy.array(box, numpy.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(image, [pts], True, (0,255,0), thickness=2)

        draw_emos(image, f, box[1])

def print_labels(response):
    resp = eval(response)
    result = resp['responses'][0]
    print json.dumps(result, indent=2, sort_keys=True)

def create_service_request(img):
    req = gc_srvs.RequestAnnotationsRequest()
    req.image = img
    req.annotations = ['FACE_DETECTION']
    req.max_results = [10]
    return req

if __name__ == '__main__':
    rospy.init_node('gc_bridge_client')

    img_msg, cv_image = get_image() 
    req = create_service_request(img_msg)
    GetAnnotationSrv = rospy.ServiceProxy('get_annotation',gc_srvs.RequestAnnotations)

    resp = GetAnnotationSrv(req)
    print_labels(resp.response)
    show_detection(cv_image, resp.response)

    cv2.imshow('modified', cv_image)

    cv2.waitKey(0)                 # Waits forever for user to press any key
    cv2.destroyAllWindows()        # Closes displayed windows
