
import argparse
import os
import sys
import httplib2
import googleapiclient
import oauth2client as oauth
from base64 import b64encode, b64decode

from cv_bridge import CvBridge, CvBridgeError

SCOPE_GOOGLECLOUDAPI = 'https://www.googleapis.com/auth/cloud-platform'
API_DISCOVERY_FILE = 'https://vision.googleapis.com/$discovery/rest?version=v1'

class Bridge(object):

    _oauth_local_token = 'oauth2.json'

    def __init__(self, client_credentials_filepath):
        self.cv_bridge = CvBridge()
        self._credentials = self._create_credentials(client_credentials_filepath)
        self._service = self._create_document(self._credentials)


    def _create_document(self, self._credentials):
        http = httplib2.Http()
        service = build('vision', 'v1', http, discoveryServiceUrl=API_DISCOVERY_FILE)

        return service


    def _create_credentials(self, client_credentials_filepath):
        '''
            Create credential object.
        '''
        storage = oauth.file.Storage(Bridge._oauth_local_token)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            flow = oauth.client.flow_from_clientsecrets(client_credentials_filepath, scope = SCOPE_GOOGLECLOUDAPI)
            parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, parents=[tools.argparser])
            flags = parser.parse_args(sys.argv[1:])
            credentials = tools.run_flow(flow, storage, flags)
        return credentials

    def request(self, msg):
        req = self._make_request(msg.image, msg.features)
        resp = self._service.images().annotate(body = req).execute()
        resp_ros = self._convert_to_ros_msg(resp)
        return resp_ros

    def _convert_to_ros_msg(self, resp):
        return resp
    

    def request_raw(self, image, features):
        request = {"requests": [{"image": { "content": b64encode(img)}, "features" : features}]}
        resp = self._service.images().annotate(body=request).execute()

        print(resp)

        return resp


    def _make_request(self, image, features):
        '''
            create a reqeust batch
        '''
        img = self.cv_bridge.imgmsg_to_cv2(image, 'bgr8')
        request_image = b64encode(img)
        request_features = [{"type":f.type, "maxResults":f.max_results} for f in features]
        request = {"requests":[{"image": { "content": request_image}, "features": request_features}]}
        return request
