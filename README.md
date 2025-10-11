Dance Pose Analysis Server
This is a lightweight Flask server that processes an uploaded video file to detect and count predefined dance poses using MediaPipe Pose. It runs the analysis frame-by-frame and returns a summary of the pose counts as a JSON object.

1. Prerequisites
Before running the server, you need to have the following software installed:

Python 3.11.x

pip (Python package installer)

2. Installation
Follow these steps to set up your environment and install the necessary dependencies.

Step 1: Clone the Repository (or save the file)
Ensure the file dance_analyzer_server.py is saved locally.

Step 2: Create a Virtual Environment (Recommended)
It is highly recommended to use a virtual environment to manage dependencies.

# Create the environment
python -m venv venv

# Activate the environment (Linux/macOS)
source venv/bin/activate

# Activate the environment (Windows)
.\venv\Scripts\activate

Step 3: Install Dependencies
This application requires Flask for the server, and OpenCV (cv2) and MediaPipe (mediapipe) for video processing and pose detection.

pip install Flask opencv-python mediapipe numpy

3. Running the Server
Once the dependencies are installed, you can start the server.

python main.py

You should see output similar to this:

Starting Dance Pose Analysis Server on [http://0.0.0.0:8080/analyze](http://0.0.0.0:8080/analyze)
 * Running on [http://0.0.0.0:8080](http://0.0.0.0:8080) (Press CTRL+C to quit)

The server is now running and listening for requests on port 8080.

4. API Usage
The application exposes a single API endpoint for video analysis.

Endpoint: /analyze
URL: http://0.0.0.0:8080/analyze

Method: POST

Content Type: multipart/form-data

Request Body
You must submit a video file using the field name video.

Parameter

Type

Required

Description

video

File

Yes

The video file (e.g., .mp4, .mov) to be analyzed.

Example Request (using curl)
You can test the endpoint by sending a POST request with a video file:

curl -X POST \
     -F "video=@/path/to/your/video.mp4" \
     [http://0.0.0.0:8080/analyze](http://0.0.0.0:8080/analyze)

(Replace /path/to/your/video.mp4 with the actual path to your video file.)

Example JSON Response
The server will respond with a JSON object summarizing the video analysis, including the total number of frames processed and the count for each detected pose.

{
    "pose_counts": {
        "Arms_Down": 120,
        "Hands_Up": 45,
        "T_pose": 10
    },
    "total_frames": 300
}

Pose Definitions
The following poses are currently tracked in the detect_dance_poses function:

Pose Name

Criteria

T_pose

Arms are roughly straight out to the sides (wrists at similar Y-coordinate) and elbows are above shoulders.

Hands_Up

Both wrists are vertically higher than their corresponding shoulders.

Arms_Down

Both wrists are vertically lower than their corresponding hips.

5. Cleanup
After the server successfully analyzes a video, it automatically deletes the temporary file and the temporary directory it created to store the uploaded video, ensuring no unnecessary files are left behind on the host system.
