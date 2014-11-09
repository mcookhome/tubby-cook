from flask import Flask,request,url_for,redirect,render_template,session
import urllib2, json
import pymongo, csv

conn=pymongo.MongoClient()
db=conn.tubbycook
accounts=db.accounts

app=Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    if 'username' in session:
        loggedin=True
        username=session['username']
    else:
        loggedin=False
        username=""
    return render_template("base.html",loggedin=loggedin, username=username)
    
@app.route("/login",methods=["GET","POST"])
def login():
    if 'username' in session:
        loggedin=True
        usern=session['username']
        return render_template("login.html",loggedin=loggedin,username=usern)
    if request.method=="POST":
        reason=""
        username=request.form['username']
        password=request.form['password']
        
        loggedin=False
        exists=False
        for d in db.accounts.find():
            if username == d['username']:
                exists=True
                savedpass=d['password']
        
        if exists==False:
            reason="The username "+username+" does not exist."
        elif savedpass==password:
            loggedin=True
        else:
            reason="Your username and password do not match"
        
        if loggedin:
            session['username']=username
        return render_template("login.html",loggedin=loggedin,username=username,reason=reason)
    else:
        return render_template("login.html", loggedin=False)
        
@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username', None)
        return render_template("logout.html",loggedin=False,prevlog=True)
    else:
        return render_template("logout.html",loggedin=False,prevlog=False) 

@app.route("/register",methods=["GET","POST"])
def register():
    if 'username' in session:
        loggedin=True
        username=session['username']
        return render_template("register.html",loggedin=loggedin,username=username)
    
    loggedin=False
    registered=False
    
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        reppassword=request.form['password2']

        reason=""
        
        if password==reppassword:
            registered=True
        else:
            registered=False
            reason="Passwords do not match"
        for d in db.accounts.find():
            if username==d['username']:
                registered=False
                reason="The username "+username+ "already exists!"
        if registered:
            doc={"username":username,"password":password}
            db.accounts.insert(doc)
            return render_template("register.html",registered=registered,username=username)
        return render_template("register.html",registered=registered, reason=reason)
    else:
        return render_template("register.html",loggedin=loggedin,registered=registered)


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
   app.secret_key="Matt<3Terrance"
   app.run()
