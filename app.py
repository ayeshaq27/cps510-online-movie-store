#!/usr/bin/env python3
from flask import Flask, render_template
from web_cs_login import cs_bp
from web_cm_login import cm_bp

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.secret_key = 'change-me'  # replace before production

    # Register blueprints
    app.register_blueprint(cs_bp, url_prefix='/cs')
    app.register_blueprint(cm_bp, url_prefix='/cm')

    @app.route('/')
    def landing():
        # Landing page with links to the login pages
        return render_template('landing.html')

    return app


if __name__ == '__main__':
    create_app().run(debug=True, port=5000)
