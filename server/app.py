#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# Clear session route
@app.route('/clear', methods=['GET'])
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

# List all articles route
@app.route('/articles', methods=['GET'])
def index_articles():
    articles = [article.to_dict() for article in Article.query.all()]
    return jsonify(articles), 200

# Show a single article and track page views
@app.route('/articles/<int:id>', methods=['GET'])
def show_article(id):
    # Set 'page_views' to 0 if it's the first request, otherwise increment it
    session['page_views'] = session.get('page_views', 0) + 1

    # If page views are within the limit, show the article
    if session['page_views'] <= 3:
        article = Article.query.filter_by(id=id).first()

        if article:
            return jsonify(article.to_dict()), 200
        else:
            return {'message': 'Article not found'}, 404

    # If page views exceed the limit, show the paywall message
    return {
        'message': 'Maximum pageview limit reached'
    }, 401

if __name__ == '__main__':
    app.run(port=5555)
