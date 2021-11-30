from flask import Flask,render_template
from tmdb import Tmdb
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

obj = Tmdb(os.getenv('TMDB_API_KEY'))

@app.route('/')
def index():
    mt = obj.get_category_list('trending','movie')
    
    tt = obj.get_category_list('trending','tv')

    mo = obj.get_category_list('now_playing', 'movie')
    to = obj.get_category_list('on_the_air', 'tv')


    return render_template('index.html',mt = mt,tt=tt,mo=mo,to=to)


@app.route('/movie/<m_id>')
def movie(m_id):
    m = obj.get_details('movie',m_id)
    k = obj.get_cast('movie',m_id)
    s = obj.get_similar('movie',m_id)

    return render_template('movie.html',m=m,k=k,s=s)


@app.route('/tv/<t_id>')
def tv(t_id):
    m = obj.get_details('tv',t_id)
    k = obj.get_cast('tv', t_id)
    s = obj.get_similar('tv', t_id)


    return render_template('movie.html', m=m,k=k,s=s)

@app.route('/person/<p_id>')
def person(p_id):
    p = obj.get_person_details(p_id)
    k = obj.get_known_for(p['title'])

    return render_template('person.html',p=p,k=k)


@app.route('/search/<query>')
def search(query):
    sm = obj.search('movie',query)
    st = obj.search('tv',query)
    sp = obj.search('person',query)

    return render_template('search.html',sm=sm,st=st,sp=sp,query=query)

@app.route('/explore/<_type>')
def explore(_type):
    t = obj.get_category_list('trending', _type)
    p = obj.get_category_list('popular', _type)

    return render_template('explore.html', t=t, p=p, _type=_type.capitalize())

@app.route('/credits')
def credits():

    return render_template('credits.html')

if __name__ == '__main__':
    app.run(debug=True)
