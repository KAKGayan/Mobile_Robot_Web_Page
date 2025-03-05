import threading
import time
import cv2  # Add the missing OpenCV import
from flask import Flask, render_template, Response
from webcamvideostream import WebcamVideoStream
from flask_basicauth import BasicAuth
import firebase_admin
from firebase_admin import credentials, db
import serial

# Initialize Flask app and Firebase
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'pi'
app.config['BASIC_AUTH_PASSWORD'] = 'pi'
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)

# Firebase setup
cred = credentials.Certificate("private_web_page.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://mywebpage-29697-default-rtdb.firebaseio.com/"
})

# Serial connection setup
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()

# Variable to track the last processed command
last_command = None

# Webcam stream function
def gen(camera):
    while True:
        if camera.stopped:
            break
        frame = camera.read()
        ret, jpeg = cv2.imencode('.jpg', frame)  # OpenCV function to encode the image
        if jpeg is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        else:
            print("frame is none")

# Flask routes
@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/monitor')
def monitor():
    return render_template('monitor.html')

@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(WebcamVideoStream().start()), mimetype='multipart/x-mixed-replace; boundary=frame')

# Firebase access function
def fetch_firebase_commands():
    global last_command
    ref = db.reference("/commands")
    while True:
        commands_dict = ref.get()
        commands_list = []
        if commands_dict:
            for key, value in commands_dict.items():
                for sub_key, sub_value in value.items():
                    commands_list.append(sub_value['command'])

        if commands_list:
            latest_command = commands_list[-1]  # Get the most recent command
            if latest_command != last_command:
                last_command = latest_command  # Update the last processed command
                print(f"New command: {latest_command}")  # Print only if it's new
        else:
            print("No commands found.")

        time.sleep(5)  # Poll the database every 5 seconds

# Main function to start threads
def run_background_tasks():
    # Start Firebase fetching in a separate thread
    firebase_thread = threading.Thread(target=fetch_firebase_commands)
    firebase_thread.daemon = True  # This allows the thread to exit when the main program exits
    firebase_thread.start()

# Main function to start Flask app
def start_flask():
    app.run(host='0.0.0.0', debug=True, threaded=True)

if __name__ == '__main__':
    run_background_tasks()  # Run background tasks like Firebase fetching
    start_flask()  # Run Flask app in the main thread
