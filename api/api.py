#coding:utf-8
__author__ = 'xus'

from util import HttpRequest,RequestMethod

class API(object):

    def __init__(self,base_api_url):
        self.request_url = base_api_url.rstrip('/')


    def __getattr__(self, item):
        self.request_url = "%s/%s" % (self.request_url,item)
        return self

    def __call__(self, *args, **kwargs):
        return "please use the 'get','post','upload' methods "

    def post(self,*args, **kwargs):
        result = HttpRequest(self.request_url,kwargs).http_post()
        return self.parse_return_json(result)

    def get(self,*args, **kwargs):
        result = HttpRequest(self.request_url,kwargs).http_get()
        return self.parse_return_json(result)

    def upload(self,*args, **kwargs):
        return HttpRequest(self.request_url,kwargs).make_url()

    def parse_return_json(self,result):
        if type(result) is not list and result.get("error_code"):
            raise APIError(result.get("error_code", ""),
                           result.get("error_msg", ""))
        return result

class APIError(StandardError):
    """API exception class."""
    def __init__(self, code, message):
        self.code = code
        StandardError.__init__(self, message)
    def __unicode__(self):
        return u"APIError: %s: %s" % (self.code, self.message)
    def __str__(self):
        return unicode(self).encode("utf-8")
