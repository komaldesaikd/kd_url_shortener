from flask import Blueprint, render_template, request, redirect
from .extensions import db
from .models import Link

shortener = Blueprint('shortener',__name__)

@shortener.route('/tier.app/')
def index():
    return render_template("index.html")

@shortener.route('/tier.app/create_link', methods=['POST'])
def create_link():
    if(request.form['original_url'] ):
        original_url = request.form['original_url']    
        link = Link(original_url=original_url)  
        print("Link1 is", link)  
        db.session.add(link)
        db.session.commit()  
    return render_template("link_success.html", new_url=link.short_url, original_url=link.original_url)    

@shortener.route('/<short_url>')
def redirect_to_url(short_url):
    if(short_url):
        link = Link.query.filter_by(short_url=short_url).first_or_404()
        link.views = link.views + 1
        db.session.commit()
    return redirect(link.original_url)     

@shortener.route('/tier.app/show', methods=['GET','POST'])
def show():
    if(request.method=='POST'):    
         short_url = request.form['short_url']    
         link = Link.query.filter_by(short_url=short_url).first_or_404()
         return render_template("show_both_link.html", short_url=link.short_url, original_url=link.original_url)   
    return render_template("show_link.html")    

@shortener.route('/tier.app/views')
def analytics():
    links = Link.query.all()
    return render_template('analytics.html', links=links)

@shortener.errorhandler(404)
def page_not_found(e):
    return ('<h1> Page Not Found 404 </h1>', 404)
