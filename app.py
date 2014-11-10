from flask import Flask,url_for,redirect,render_template,session
from flask import request
import urllib2, json

app=Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("base.html")

@app.route("/t", methods=['GET', 'POST'])
def t():
    if request.method == "POST":
        tag= request.form['tag']
        location=request.form['loc']
        tag=tag.replace(" ", "+")
        location=location.replace(" ", "+")
        print tag
        print location
        url = "http://api.yelp.com/v2/search?term="+tag+"&location="+location
        print url
        req = urllib2.urlopen(url)
        res_string = req.read()
        d = json.loads(res_string)
        return "<h1>hello</h1>"
    else:
        return render_template("base.html")




if __name__=="__main__":
   app.debug=True
   app.secret_key="Matt<3Terrance"
   app.run()
