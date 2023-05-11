from flask import Flask
from routes import *

# Create the Flask application instance
app = Flask(__name__)

# Register your routes
app.register_blueprint(routes)

# Optionally, configure any necessary Flask settings
app.config['DEBUG'] = True

# Start the Flask development server
if __name__ == '__main__':
    app.run()