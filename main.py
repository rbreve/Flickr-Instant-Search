from google.appengine.api import urlfetch 
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import os
from google.appengine.ext.webapp import template
from django.utils import simplejson as json
import logging
from urllib import quote

API_KEY = 'fc23feb20ac7ad45c9a55caee601bf65'
API_SECRET = '2cc87c9c98d01d9b'

class Flickr(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'flickr.htm')
        self.response.out.write(template.render(path,[]))
       

class GetFlickr(webapp.RequestHandler):
    def get(self):
        q=self.request.get('q')
        t=self.request.get('t')
        c=self.request.get('c')
        o=self.request.get('o')
        
        if(o=="recent"):
            o="&sort=date-posted-desc"
            
        if(o=="relevance"):
            o="&sort=relevance"
        
        if(o=="interesting"):
            o="&sort=interestingness-desc"
            
        if(t):
            tags=q.split(" ")
            t="&tags=" + ",".join(tags)
            q=""
        if(c):
            c="&is_commons=1"
        
        q=quote(q)


        url="http://api.flickr.com/services/rest/?method=flickr.photos.search&format=json&api_key=%s&text=%s&nojsoncallback=1&per_page=20%s%s%s" % (API_KEY,q,t,c,o)
        r=urlfetch.fetch(url)
        logging.info(url)
        obj=json.loads(r.content)
        photos=obj['photos']['photo']
    
        p="["
        for photo in photos:
             p+='{"id":"%s","user_id":"%s","photo":"http://farm%s.static.flickr.com/%s/%s_%s_m.jpg"},'%(photo['id'],photo['owner'],photo['farm'], photo['server'],photo['id'],photo['secret'])
        p=p[:-1]+"]"
        self.response.out.write(p)

class MainHandler(webapp.RequestHandler):
    
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.htm')
        self.response.out.write(template.render(path,[]))
    
         
def main():
    application = webapp.WSGIApplication(
                                        [('/', MainHandler),
                                        ('/gf', GetFlickr),
                                        ('/flickr', Flickr)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
