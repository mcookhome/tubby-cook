from flask import Flask,url_for,redirect,render_template,session,request
import urllib2, json
import oauth2

app=Flask(__name__)

CONSUMER_KEY='q2XZ_XmBad4V6QqitVZvQg'
CONSUMER_SECRET='Sf9Zmq2H8EeiajdcSKXQPSBDcuM'
TOKEN='EIUZN8Qk17u0o1GrccKcuUHnZcVlz2LD'
TOKEN_SECRET='LTJDS6mS7yr4EfVWYL4LiwhzIXI'



def req(url_params=None):
    url_params = url_params or {}
    url='http://{0}{1}?'.format('api.yelp.com','/v2/search/')
    
    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET",url=url, parameters=url_params)
    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url=oauth_request.to_url()
    print 'Querying {0} ...".format(url)'
    conn=urllib2.urlopen(signed_url, None)
    response = json.loads(conn.read())
    conn.close()
    return response

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("base.html")

@app.route("/t", methods=['GET', 'POST'])
def t():
    if request.method == "POST":
        tag= request.form['tag']
        location=request.form['loc']
        url_params ={'term':tag.replace(" ", "+"),'location':location.replace(" ", "+"), 'limit': 5, 'category_filter': 'food'}
        for x in req(url_params)['businesses']:
            print x[u'name']+" - "+x[u'snippet_text'].replace("\n"," ")
        return "<h1>hello</h1>"
    else:
        return render_template("base.html")




if __name__=="__main__":
   app.debug=True
   app.secret_key="Matt<3Terrance"
   app.run()
