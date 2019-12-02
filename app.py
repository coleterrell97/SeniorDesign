from flask import Flask, render_template, Response, request, jsonify
import json
app = Flask(__name__)

CONFIG_SETTINGS = {
        "SWAP_CAMERAS": 0,
        "VERTICAL_FLIP": 0,
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

# Video streaming home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/update_values", methods=["POST"])
def update_values():
    v = int(request.form.get("SWAP_CAMERAS"))
    u = int(request.form.get("VERTICAL_FLIP"))
    print("!!!!!!!")
    print(v)
    print(u)

    # Get and update values from the settings page
    for prop in CONFIG_SETTINGS.keys():
        CONFIG_SETTINGS[prop] = int(request.form.get(prop))

    # Write the values to the config file
    with open(CONFIG_FILE, "w") as f:
        f.write(json.dumps(CONFIG_SETTINGS))

    return render_template('index.html')

@app.route("/send_values", methods=["GET"])
def send_values():
    return jsonify(CONFIG_SETTINGS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)
