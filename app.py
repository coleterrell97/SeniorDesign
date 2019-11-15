from flask import Flask, render_template, Response, request
import json

app = Flask(__name__)
CONFIG_SETTINGS = {
        "CAP_PROP_BRIGHTNESS" : 0,
        "CAP_PROP_CONTRAST" : 15,
        "CAP_PROP_SATURATION" : 32,
        "CAP_PROP_SHARPNESS" : 16,
        "CAP_PROP_GAMMA" : 220,
        "CAP_PROP_WHITE_BALANCE_BLUE_U" : 5000,
        "CAP_PROP_GAIN" : 0,
        "CAP_PROP_PAN" : 0,
        "CAP_PROP_TILT" : 0,
        "CAP_PROP_ZOOM" : 100,
        "CAP_PROP_EXPOSURE" : 312,
        "CAP_PROP_BACKLIGHT" : 0,
        "CAP_PROP_ROLL" : 0,
        "CAP_PROP_IRIS" : 0,
        "CAP_PROP_FOCUS" : 0,
        "CAP_PROP_HUE" : 0
    }

SETTINGS_PAGE = 'settings.html'
CONFIG_FILE = 'config.json'


# Settings page homepage
@app.route('/')
def index():
    return render_template('settings.html')

# Accepts POST request to update config file values
@app.route("/", methods=["POST"])
def update_values():
    # Get and update values from the settings page
    for prop in CONFIG_SETTINGS.keys():
        CONFIG_SETTINGS[prop] = int(request.form.get(prop))

    # Write the values to the config file
    with open(CONFIG_FILE, "w") as f:
        f.write(json.dumps(CONFIG_SETTINGS))

    return render_template('settings.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)
