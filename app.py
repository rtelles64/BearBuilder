import json  # to save form info to a json file (i.e. cookies)
from flask import (Flask, render_template, redirect, url_for, request,
                   make_response, flash)
from options import DEFAULTS

app = Flask(__name__)
# Since sessions are signed with an encrypted key, create one in order to
# display a flash message for our session
# Keys are best when they are random and long
app.secret_key = "hahdfouher725hlsdhae2hhi#$%^hshf"


def get_saved_data():
    '''
        Retrieves data from cookie
    '''
    # .dumps(): creates a json string
    # .loads(): takes that string and turns it into python code again
    try:
        data = json.loads(request.cookies.get('character'))
    except TypeError:
        data = {}
    return data


@app.route('/')
def index():
    return render_template('index.html', saves=get_saved_data())


@app.route('/builder')
def builder():
    return render_template(
        'builder.html',
        saves = get_saved_data(),
        options = DEFAULTS
    )


# method: POST -- Only access /save if you post to it
@app.route('/save', methods=['POST'])
def save():
    # flash a message to indicate settings have been saved
    # The message will be gone if a session is refreshed
    flash("Alright! That looks awesome!")
    # set cookie
    response = make_response(redirect(url_for('builder')))
    # Using cookies is good when we're only using local storage and not a
    # database
    # call the cookie 'character'
    # .items(): returns the key,value pairs from request.form (recall it's an
    #           ImmutableMultiDict object)
    # .dumps(): so we turn the form items into a dict, and dump them into a
    #           json file
    # NOTE: dumps means "dump string"
    # NOTE: You can check the cookie in the Storage tab of the web inspector
    #       in browser
    data = get_saved_data()
    # update cookie
    # RECALL: Cookies need to be strings
    data.update(dict(request.form.items()))
    response.set_cookie('character', json.dumps(data))
    return response


app.run(debug=True, host='0.0.0.0', port=8000)
