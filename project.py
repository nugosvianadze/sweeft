from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

import random
import string

# Create the Flask app
app = Flask(__name__)

# Set up the database
engine = create_engine('sqlite:///urls.db')
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


def generate_short_name(length=8):
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for i in range(length))


def is_valid_url(url):
    return url.startswith('http://') or url.startswith('https://') and len(url) <= 250


class URL(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    original_url = Column(String(250), nullable=False)
    short_name = Column(String(8), nullable=False, unique=True)
    custom_name = Column(String(50), nullable=True, unique=True)
    access_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    def is_expired(self):
        return self.created_at < datetime.utcnow() - timedelta(days=30)


Base.metadata.create_all(engine)


# Define the API endpoints
@app.route('/url', methods=['POST'])
def create_url():
    # Parse the input URL from the request body
    input_url = request.json.get('url')
    if not input_url:
        return jsonify({'error': 'URL is missing'}), 400

    # Validate the input URL
    if not is_valid_url(input_url):
        return jsonify({'error': 'Invalid URL'}), 400

    # Generate a random short name and check if it's available
    short_name = generate_short_name()
    while session.query(URL).filter_by(short_name=short_name).first() is not None:
        short_name = generate_short_name()

    # Insert the URL into the database
    url = URL(original_url=input_url, short_name=short_name)
    session.add(url)
    session.commit()

    # Return the shortened URL
    return jsonify({'url': f'/url/{short_name}'}), 201


@app.route('/url/<short_name>', methods=['GET'])
def get_url(short_name):
    # Get the URL from the database
    url = session.query(URL).filter_by(short_name=short_name).first()
    if url is None:
        return jsonify({'error': 'URL not found'}), 404

    # Update the access count
    url.access_count += 1
    session.commit()

    # Return the original URL
    return jsonify({'url': url.original_url}), 200


@app.route('/url/<custom_name>', methods=['POST'])
def create_custom_url(custom_name):
    # Parse the input URL from the request body
    input_url = request.json.get('url')
    if not input_url:
        return jsonify({'error': 'URL is missing'}), 400

    if not is_valid_url(input_url):
        return jsonify({'error': 'Invalid URL'}), 400

    # Check if the custom name is available
    if session.query(URL).filter_by(custom_name=custom_name).first() is not None:
        return jsonify({'error': 'Custom name already taken'}), 409

    # Insert the URL into the database
    url = URL(original_url=input_url, custom_name=custom_name)
    session.add(url)
    session.commit()

    # Return the shortened URL
    return jsonify({'url': f'/url/{custom_name}'}), 201


# delete expired urls
@app.route('/delete_expired_urls')
def delete_expired_urls():
    session.query(URL).filter(URL.is_expired()).delete()
    session.commit()
    return 'Expired URLs deleted'

# delete expired urls in background
scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_expired_urls, trigger='interval', days=1)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)
