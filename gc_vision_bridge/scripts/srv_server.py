#!/usr/bin/env python

import rospy
import gc_vision_bridge
import gc_msgs.srv as gc_srvs

class VisionBridgeServiceServer(object):
    '''
      Current implementation only accepts one image per request.
      Later, it can be improved to accept multiple images.
    '''

    def __init__(self):
        self._srv_name = "get_annotation"
        self._bridge = gc_vision_bridge.VisionBridgeROS()
        self._srv = rospy.Service("get_annotation",gc_srvs.RequestAnnotations, self._process_image)

    def _process_image(self, msg):
        resp = self._bridge.request(msg.image, msg.features)
        return gc_srvs.RequestAnnotationsResponse(resp)

    def spin(self):
        rospy.spin()

    def loginfo(self, msg):
        m = "%s : %s"%("Vision Bridge", str(msg))
        rospy.loginfo(m)

if __name__ == '__main__':
    rospy.init_node("gc_bridge_server")

    bridge = VisionBridgeServiceServer()
    bridge.loginfo("Initialised")
    bridge.spin()
    bridge.loginfo("Bye Bye")
