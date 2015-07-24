from flask import Flask, render_template
import urllib2
import json

module=Flask(__name__)

def  flickr(query='<search>'):
    url='https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=9ec60a6f3b8f6c88b1d05f386106ae5e&tags=%s&format=json&nojsoncallback=1'%query
    u = urllib2.urlopen(url)
    result=u.read()
    w=json.loads(result)
    return w['photos']['photo']

@module.route('/')
@module.route('/<search>')
def Pickles(search='pickle'):
    try:
        return render_template('Pickles.html',image=flickr(search))
    except:
        return render_template('Error.html',error='This picture does not exist')


if __name__=='__main__':
    module.debug=True
    module.run()
    
