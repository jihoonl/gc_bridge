
import argparse
import os
import sys
import httplib2
import googleapiclient
import oauth2client as oauth

SCOPE_GOOGLECLOUDAPI = 'https://www.googleapis.com/auth/cloud-platform'

class Bridge(object):

    _oauth_local_token = 'oauth2.json'

    def __init__(self, client_credentials_filepath):

        self._credentials = self._create_credentials(client_credentials_filepath)
        self._bridge = googleapiclient.discovery.build('vision', 'v1', credentials=credentials, discoveryServiceUrl= 



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
