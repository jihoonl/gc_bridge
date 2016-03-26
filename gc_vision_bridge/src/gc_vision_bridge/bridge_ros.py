
from base64 import b64encode, b64decode, encodestring
from cv_bridge import CvBridge, CvBridgeError
from io  import BytesIO

from PIL import Image
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
        return resp

    def _make_request(self, img_msg, features):
        '''
            create a reqeust batch
        '''
        img = self.cv_bridge.imgmsg_to_cv2(img_msg, 'bgr8')
        ii = Image.fromarray(img)
        buff = BytesIO()
        ii.save(buff, format="JPEG")
        request_image = b64encode(buff.getvalue())
        request_features = [{"type":f['type'], "maxResults":f['maxResults']} for f in features]
        request = {"requests":[{"image": { "content": request_image}, "features": request_features}]}
        return request
