from flask import Flask, render_template, Response, session, request
import cv2
import os
import csv

from Alex_Santos.streaming_func import process_frame

app = Flask(__name__)
app.config["SECRET_KEY"] = "dkVdso$#97298Df903jsDFSD?"

camera = cv2.VideoCapture(0)

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            frame = process_frame(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


# setting up a session for storing filename
@app.before_first_request
def first_request():
    session["filename"] = "streaming_data.csv"


# route with post request for changing filename
@app.route("/change_filename", methods=["POST", "GET"])
def change_filename():
    filename = request.get_data('filename')
    session['filename'] = filename.decode("utf-8")
    write_header(session['filename'])
    with open("Alex_Santos/fl.txt", "w", encoding='utf-8') as f:
        f.write(session['filename'])
    return ""


def write_header(filename):
    #headers for our CSV file
    header = ['Timestamp', 'Right_Arm_Angle', 'Left_Arm_Angle', 'Right_Leg_Angle',  'Left_Leg_Angle',
                'Nose', 'Left Inner Eye', 'Left Eye', 'Left Outter Eye', 'Right Inner Eye', 
                'Right Eye', 'Right Outter Eye', 'Left Ear', 'Right Ear', 'Mouth Left', 'Mouth Right',
                'Left Shoulder', 'Right Shoulder', 'Left Elbow', 'Right Elbow', 'Left Wrist', 
                'Right Wrist', 'Left Pinky', 'Right Pinky', 'Left Index', 'Right Index', 
                'L-Thmb', 'R-Thmb', 'L Hip', 'sR Hip', 'L-Knee', 'R-Knee', 'L-Ankle', 'R-Ankle', 
                'L-Heel', 'R-Heel', 'L-Foot-Index', 'R-Foot-Index']
    filename = filename
    file_existance = os.path.exists(filename)
    csv_file = open(filename, mode="a+", encoding="utf-8", newline="")
    writer = csv.DictWriter(csv_file, fieldnames=header)

    if not file_existance:
        writer.writeheader()
    csv_file.close()

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)