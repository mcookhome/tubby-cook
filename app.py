from flask import Flask,url_for,redirect,render_template,session,request
import urllib2, json,unicodedata
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
    print signed_url
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

        page = ""
        for x in req(url_params)['businesses']:
            print x[u'name']+" - "+x[u'snippet_text'].replace("\n"," ")
            page += x[u'name']+" - "+x[u'snippet_text'].replace("\n"," ") + "<br>"
        return page
    else:
        return render_template("base.html")

@app.route("/spot", methods=['GET', 'POST'])
def spot():
    stri="Dianda's Italian American Pastry"
    L=stri.split()
    L[:] = [ urlify(o) for o in L]
    print L
    k = 20/len(L)-1
    i=0
    songids=[]
    for n in L:
        print n
        conn=urllib2.urlopen(n, None)
        response = json.loads(conn.read())
        conn.close()
        ppp= response['tracks']['items']
        for m in ppp:
            song = m['id']
            print song
            songids.append(song)
            print "i: "+str(i)
            print "k: "+str(k)
            if i == k:
                print"broken"
                i=0
                break
            else:
                i = i+1
    print songids
    songids[:]=[unicodedata.normalize('NFKD',o).encode('ascii','ignore') for o in songids]
    print songids
    tracklist=""
    for n in songids:
        tracklist += n + ","
    tracklist = tracklist[:-1]
    print "dingdong"+tracklist
        
    return render_template("spotify.html", s=tracklist)
    
def urlify(s):
    url = "https://api.spotify.com/v1/search?q=" +s+ "&type=track"
    return url

if __name__=="__main__":
   app.debug=True
   app.secret_key="Matt<3Terrance"
   app.run()
