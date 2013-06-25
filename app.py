import os 
from flask import Flask, render_template, request, redirect,url_for,session, g, make_response, send_from_directory
import uuid

from recommendationEngine import *
app = Flask(__name__) #, static_folder="./static", static_url_path="/static")

app.config.update(
    DEBUG = True,
)

@app.route('/' ,methods=["GET", "POST"])
def index():
    #g.i = 0 

    if request.method == "POST": 
        
        print request.form
        if request.form['uname'] != '':
            uname = request.form['uname']
            session['uname'] = request.form['uname']
            session['uid'] = request.form['uname'] +'_'+ uuid.uuid1().hex
            
            return redirect(url_for('submit'))

        else:
           
            return render_template('theIndex.jinja2.html',page_submit="active")
    else:   
        
        return render_template('theIndex.jinja2.html',page_submit="active")

@app.route('/submit/' ,methods=["POST","GET"])
def submit():
    #print "list", g.movies
    #g.i += 1 
    #print "iii", i 
    print session['uid']
    uname = session['uname']
    print uname
    #g.movie = {u'title':'blah blah'}
   # return render_template('myindex.jinja2.html',page_submit="active", uname=uname)

    movie = random_movie()  
    #movs += [movie]
    #return render_template('myindex.jinja2.html',page_submit="active", movie=movie, uname=uname)
    if request.method == "POST":
        #movie = random_movie()             
        return do_submit(uname,movie)
        
    else:
        #movie = random_movie()
        return render_template('myindex.jinja2.html',page_submit="active", uname=uname, movie=movie)
    

@app.route('/about/')
def about():
    return render_template('about.jinja2.html')

# # @app.after_request
# # def get_movie(response):
# #     movie = random_movie() 
# #     print "gg", movie
# #     return response


@app.before_request
def get_movie():
    g.movie = random_movie()
#     #g.old = g.movie

# #     #print "gg", movie
# #     #return response

# # @app.after_request
# # def get_movie_again(response):
# #     g.movie = g.old
# #     print g.old
# #     return(response)

def do_submit(uname,movie):
    import HTMLParser 
    p = HTMLParser.HTMLParser()
    form = request.form
    print "len", len(form.values()[0])
    rating = {}
    score = 0 
    print "form values", form.values()
    nrecords = 0
    if len(form.values()[0]) > 0: 
    #    
    #    return render_template('myindex.jinja2.html', page_submit="active", uname=uname,movie=movie)      
    #else:
        
        score = eval(form.values()[0])
        print score
        rating['uid'] = session['uid']
        rating['title'] = (p.unescape(form.keys()[0])).decode('utf-8')
        rating['score'] = score
        
        print rating 
        
        #print "ggg", g.movie
        #mongo db call
        nrecords = insert_rating(rating)
        print "You have rated %d movies"%nrecords
	    
    if (nrecords < 20):
    	enough = False   
    	return render_template('myindex.jinja2.html', page_submit="active", uname=uname,movie=movie)
    else:
    	return render_template('myindex.jinja2.html',page_submit="active", uname=uname,movie=movie,enough=True) 





@app.route('/reco/')
def reco():
    rows = {} 
    uname = session['uname']  
    rankings = get_recommendation(session['uid'])
    print rankings
    rows = []
    for prediction, title in rankings:
        row = {}
        row['title'] = title
        row['prediction']  = "%3.2f"%prediction
        rows += [row]
    print rows
    return render_template('reco.jinja2.html', rows = rows, uname = uname)
    
# @app.context_processor
# def utility_processor():
#   def get_random_movie():
#     g.movie = random_movie()['title']
#     return g.movie
#   return dict(get_random_movie=get_random_movie)

app.secret_key = '\xaezX\xc7\xb2\x8d\xf7\x03~\xc1\xae\x0emn\x9aO\xc9$\xa8\x140\x0c\xdd'
#def run_devserver():
#    app.run(debug=True)

#if __name__ == "__main__":
#    run_devserver()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
