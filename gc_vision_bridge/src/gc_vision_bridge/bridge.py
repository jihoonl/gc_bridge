
import argparse
import os
import sys
import httplib2
from googleapiclient import discovery as googleapidiscovery
from oauth2client.client import GoogleCredentials

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


    def _create_document(self, credentials):
        service = googleapidiscovery.build('vision', 'v1', credentials=credentials, discoveryServiceUrl=API_DISCOVERY_FILE)
        return service


    def _create_credentials(self, client_credentials_filepath):
        '''
            Create credential object.
        '''
        credentials = GoogleCredentials.get_application_default()
        return credentials

    def request(self, msg):
        req = self._make_request(msg.image, msg.features)
        resp = self._service.images().annotate(body = req).execute()
        resp_ros = self._convert_to_ros_msg(resp)
        return resp_ros

    def _convert_to_ros_msg(self, resp):
        return resp

    def request_raw(self, image, features):
        request = {"requests": [{"image": { "content": b64encode(image)}, "features" : features}]}
        resp = self._service.images().annotate(body=request).execute()
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
