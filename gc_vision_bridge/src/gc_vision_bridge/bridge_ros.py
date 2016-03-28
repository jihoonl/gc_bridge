
from base64 import b64encode, b64decode, encodestring
from cv_bridge import CvBridge, CvBridgeError
import cStringIO 

import cv2
from PIL import Image
from .bridge import VisionBridge
import ast, json

SCOPE_GOOGLECLOUDAPI = 'https://www.googleapis.com/auth/cloud-platform'
API_DISCOVERY_FILE = 'https://vision.googleapis.com/$discovery/rest?version=v1'

class VisionBridgeROS(VisionBridge):

    def __init__(self):
        super(VisionBridgeROS, self).__init__()

        self.cv_bridge = CvBridge()

    def request(self, image, features):
        req_img = self._encode_rosimage_to_b64(image)
        req_features = self._create_features(features)
        request = {"requests":[{"image": { "content": req_img}, "features": req_features}]}

        resp = self._service.images().annotate(body = request).execute()

        # convert unicode string to ascii
        r = ast.literal_eval(json.dumps(resp))
        return r

    def _encode_rosimage_to_b64(self, image):
        img = self.cv_bridge.imgmsg_to_cv2(image, 'rgb8')
        ii = Image.fromarray(img)
        buff = cStringIO.StringIO()
        ii.save(buff,'JPEG')
        buff.seek(0)
        request_image = b64encode(buff.getvalue())

        # self._save_test_image(buff)
        return request_image

    def _save_test_image(self, buff):
        gg = cStringIO.StringIO(buff.getvalue())
        cimg = Image.open(gg)
        cimg.save('hola.jpg','JPEG')

    def _create_features(self, features):
        request_features = [{"type":f['type'], "maxResults":f['maxResults']} for f in features]
        return request_features
