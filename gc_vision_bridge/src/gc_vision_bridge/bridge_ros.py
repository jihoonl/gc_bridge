
from base64 import b64encode, b64decode
from cv_bridge import CvBridge, CvBridgeError
from .bridge import VisionBridge

SCOPE_GOOGLECLOUDAPI = 'https://www.googleapis.com/auth/cloud-platform'
API_DISCOVERY_FILE = 'https://vision.googleapis.com/$discovery/rest?version=v1'

class VisionBridgeROS(VisionBridge):

    def __init__(self):
        super(VisionBridgeROS, self).__init__()

        self.cv_bridge = CvBridge()

    def request(self, image, features):
        req = self._make_request(image, features)
        resp = self._service.images().annotate(body = req).execute()
        resp_ros = self._convert_to_ros_msg(resp)
        return resp_ros

    def _make_request(self, image, features):
        '''
            create a reqeust batch
        '''
        img = self.cv_bridge.imgmsg_to_cv2(image, 'bgr8')
        request_image = b64encode(img)
        request_features = [{"type":f.type, "maxResults":f.max_results} for f in features]
        request = {"requests":[{"image": { "content": request_image}, "features": request_features}]}
        return request
