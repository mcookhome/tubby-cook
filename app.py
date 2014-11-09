from flask import Flask,request,url_for,redirect,render_template
import urllib2, json

app=Flask(__name__)

@app.route("/")
def index():
    return "hello"

@app.route("/t")
@app.route("/t/<tag>")
def t(tag="cream puffs"):
        tag.replace(" ", "+")
	url = "http://api.yelp.com/v2/search?term=%s&location=San+Francisco"
	url = url%(tag)
	request = urllib2.urlopen(url)
	res_string = request.read()
	d = json.loads(res_string)
	page = ""
	for r in d['response']:
		if 'photos' in r.keys():
			page = page +"<img height=200 src=%s>"%(r['photos'][0]['original_size']['url'])
	return page


if __name__=="__main__":
   app.debug=True
   app.run()
