from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, jsonify, Blueprint 
import json
import os.path
from werkzeug.utils import secure_filename

bp = Blueprint('urlshort', __name__)

@bp.route("/")
def home():
    return render_template('home.html', codes=session.keys())

@bp.route("/your-url", methods=['GET', "POST"])
def your_url():
    if request.method == 'POST':
        urls = {}

        # Use the correct file name and check if it exists
        if os.path.exists('url.json'):
            with open('url.json') as url_file:
                urls = json.load(url_file)

        if request.form['code'] in urls.keys(): 
            flash('Oops! that name is already taken. Please select another one')
            return redirect(url_for('urlshort.home'))      

        if 'url' in request.form.keys():  
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            f = request.files['file']  
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('/Users/suveer/Desktop/url-shortner/urlshort/static/user_files/' + full_name)
            urls[request.form['code']] = {'file': full_name}

        # Write back to the file
        with open('url.json', 'w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True
        
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('urlshort.home'))

@bp.route("/<string:code>")
def redirect_to_url(code):
    if os.path.exists('url.json'):
        with open('url.json') as url_file:
            urls = json.load(url_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
    
    return abort(404)

@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404

@bp.route("/api")
def session_api():
    return jsonify(list(session.keys()))

# Factory function to create the app
def create_app():
    app = Flask(__name__)
    app.secret_key = 'S1v2u3e4e5r6'  # Set your secret key
    app.register_blueprint(bp)  # Register the Blueprint
    app.config['DEBUG'] = True  # Enable debug mode

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
