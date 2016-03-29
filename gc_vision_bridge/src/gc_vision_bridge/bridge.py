
from googleapiclient import discovery as googleapidiscovery
from oauth2client.client import GoogleCredentials

from base64 import b64encode, b64decode

SCOPE_GOOGLECLOUDAPI = 'https://www.googleapis.com/auth/cloud-platform'
API_DISCOVERY_FILE = 'https://vision.googleapis.com/$discovery/rest?version=v1'

class VisionBridge(object):
    '''
      Simple Python wrapper to communicate with google cloud vision
    '''

    def __init__(self):
        self._credentials = self._create_credentials()
        self._service = self._create_document(self._credentials)

    def _create_document(self, credentials):
        service = googleapidiscovery.build('vision', 'v1', credentials=credentials, discoveryServiceUrl=API_DISCOVERY_FILE)
        return service

    def _create_credentials(self):
        '''
          Create credential instance using default GoogleCredentials. check your env GOOGLE_APPLICATION_CREDENTIALS
        '''
        credentials = GoogleCredentials.get_application_default()
        return credentials

    def request_raw(self, image, features):
        '''
        :param image: image byte array
        :param features: feature json
        '''
        request = {"requests": [{"image": { "content": b64encode(image)}, "features" : features}]}
        resp = self._service.images().annotate(body=request).execute()
        return resp
