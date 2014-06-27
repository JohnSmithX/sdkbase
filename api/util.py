__author__ = 'xus'

import urllib,urllib2,json,time

class RequestMethod:
    GET=1
    POST=2
    UPLOAD=3

class JSONMap(object):
    def __init__(self,json_file,type_of_API):
        self._json_file = json_file
        self._API_type = type_of_API
        self._json = self.read_from_json_file( self._json_file)

    @classmethod
    def read_from_json_file(self,file):
        try:
            f=open(file,'r')
            return json.load(f)
        except IOError,e:
            raise e
        finally:
            f.close()

    @classmethod
    def read_from_json(self,json):
        pass

    def parse_json(self):
        return self._json[self._API_type]

class HttpRequest(object):

    def __init__(self,url,params={},**kwargs):
        self.request_url = url
        self.params = params
        self.request_obj = ''
        self.wrap_params()

    def wrap_params(self):
        if self.params:
            self.params = self.encode_params(self.params)
        else:
            self.params = ""

    def http_get(self):
        self.request_obj = urllib2.Request(self.make_url())
        return self.send_request()

    def http_post(self):
        self.request_obj = urllib2.Request(self.request_url, data=self.params)
        return self.send_request()

    def http_upload(self):
        pass

    def http_method(self,method):
        if method == RequestMethod.GET:
            return self.http_get()
        elif method == RequestMethod.POST:
            return self.http_post()
        else:
            return self.http_upload()

    def make_url(self):
        return "%s?%s" % (self.request_url, self.params)

    def send_request(self):
        try:
            resp = urllib2.urlopen(self.request_obj)
            content = resp.read()
            result = json.loads(content)
            return result
        except urllib2.HTTPError as e:
            raise e


    def encode_str(self,obj):
        if isinstance(obj, basestring):
            return obj.encode("utf-8") if isinstance(obj, unicode) else obj
        return str(obj)

    def encode_params(self,params):
        return "&".join(["%s=%s" % (k, urllib.quote(self.encode_str(v)))
                         for k, v in params.iteritems()])

    def encode_multipart(self,filename=None, **kw):
        boundary = "----------%s" % hex(int(time.time() * 1000))
        params = []
        for k, v in kw.iteritems():
            params.append("--%s" % boundary)
            if hasattr(v, "read"):
                content = v.read()
                if hasattr(v, "name") and filename is None:
                    filename = v.name
                params.append("Content-Disposition: form-data; name=\"%s\";"
                              "filename=\"%s\"" % (k, filename))
                params.append("Content-Type: %s\r\n" %
                              self.guess_content_type(filename))
                params.append(content)
            else:
                params.append("Content-Disposition: form-data; name=\"%s\"\r\n"
                              % k)
                params.append(self.encode_str(v))
            params.append("--%s--\r\n" % boundary)
            return "\r\n".join(params), boundary

    def guess_content_type(self,name):
        if name.endswith(".jpg"):
            return "image/jpg"
        elif name.endswith(".jpeg"):
            return "image/jpeg"
        elif name.endswith(".png"):
            return "image/png"
        elif name.endswith(".gif"):
            return "image/gif"
        elif name.endswith(".bmp"):
            return "image/bmp"
        return "image/jpg"