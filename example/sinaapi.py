#coding:utf-8
__version__ = '1.0.0'
__author__ = 'xus'

import  os
from api.api import API
from api.util import JSONMap,HttpRequest



class SinaAPIClient(API):
    def __init__(self,json_file,type_of_API="sina",*args,**kwargs):
        self._config=JSONMap(json_file,type_of_API)
        for key,value in self._config.parse_json().iteritems():
            setattr(self,key,value)
        super(SinaAPIClient,self).__init__(self.base_api_url)


    def get_authorize_url(self,*args,**kwargs):
        params = dict(client_id=self.api_key,response_type=self.response_type,redirect_uri=self.callback_url)
        url = '%s%s' % (self.base_oauth_url, 'authorize')
        return HttpRequest(url,params).make_url()


    def get_access_token(self):
        pass


f=os.path.join(os.path.dirname(__file__),"weibo.json")
a=SinaAPIClient(f)

print a.metions.to_me.upload(callback='http://www.catme.net',access_torken ='12313456')
