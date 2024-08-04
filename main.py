import os
import paramiko
from flask import Flask, render_template, request, jsonify
import openai
import cv2
import logging
import uuid

app = Flask(__name__)

# SSH connection details
SSH_HOST = '4.tcp.ngrok.io'  # Replace with your Raspberry Pi IP
SSH_PORT = 11289             # Replace with the forwarded SSH port
SSH_USER = 'samnu'           # Replace with your Raspberry Pi username
SSH_PASSWORD = 'Simsim500**' # Replace with your Raspberry Pi password
REMOTE_BASE_PATH = 'home/samnu'

# Ensure the 'uploads' directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Set your OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def ssh_execute_command(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)
    stdin, stdout, stderr = ssh.exec_command(command)
    stdout.channel.recv_exit_status()  # Wait for command to finish
    ssh.close()

def ssh_upload_file(local_path, remote_path):
    # Ensure remote directory exists
    remote_dir = os.path.dirname(remote_path)
    ssh_execute_command(f'mkdir -p {remote_dir}')

    # Upload file
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)
    sftp = ssh.open_sftp()
    logging.debug(f"Uploading {local_path} to {remote_path}")
    sftp.put(local_path, remote_path)
    sftp.close()
    ssh.close()
    logging.debug(f"Uploaded {local_path} to {remote_path}")

def ssh_download_file(remote_path, local_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)
    sftp = ssh.open_sftp()
    sftp.get(remote_path, local_path)
    sftp.close()
    ssh.close()

def extract_frames_and_upload(video_path, session_id):
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0
    frame_interval = 100  # Save every 100 frame
    saved_count = 0

    # Define the desired width and height for the resized frames
    desired_width = 640
    desired_height = 480
    jpeg_quality = 20  # JPEG quality (0-100), where lower means higher compression

    local_frames_path = os.path.join('frames', session_id)
    remote_frames_path = os.path.join(REMOTE_BASE_PATH, 'frames', session_id)

    if not os.path.exists(local_frames_path):
        os.makedirs(local_frames_path)

    while success:
        if count % frame_interval == 0:
            # Resize the image to the desired resolution
            resized_image = cv2.resize(image, (desired_width, desired_height), interpolation=cv2.INTER_AREA)

            frame_path = os.path.join(local_frames_path, f"frame{saved_count}.jpg")

            # Save the resized frame with reduced JPEG quality
            cv2.imwrite(frame_path, resized_image, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])

            # Upload frame to Raspberry Pi
            ssh_upload_file(frame_path, os.path.join(remote_frames_path, f"frame{saved_count}.jpg"))

            # Delete local frame file after uploading
            os.remove(frame_path)

            saved_count += 1

        success, image = vidcap.read()
        count += 1

    vidcap.release()
    return saved_count

def analyze_frame(frame_path):
    # Placeholder function for frame analysis
    # Implement your own analysis logic here
    return "Frisbee detected in frame. Throw angle looks good."

def summarize_analysis(frame_count, session_id):
    summaries = []
    local_frames_path = os.path.join('frames', session_id)
    remote_frames_path = os.path.join(REMOTE_BASE_PATH, 'frames', session_id)

    if not os.path.exists(local_frames_path):
        os.makedirs(local_frames_path)

    for i in range(frame_count):
        remote_frame_path = os.path.join(remote_frames_path, f"frame{i}.jpg")
        local_frame_path = os.path.join(local_frames_path, f"frame{i}.jpg")

        # Download frame from Raspberry Pi
        ssh_download_file(remote_frame_path, local_frame_path)

        # Analyze frame
        summary = analyze_frame(local_frame_path)
        summaries.append(summary)

        # Delete local frame file after analyzing
        os.remove(local_frame_path)

    return " ".join(summaries)

def get_feedback_from_gpt4(summary):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in analyzing ultimate frisbee throws."},
            {"role": "user", "content": summary}
        ],
        max_tokens=150,
        temperature=0.7
    )
    feedback = response['choices'][0]['message']['content'].strip()
    return feedback

@app.route('/')
def index():
    return render_template('index.html')

import shutil

@app.route('/analyze', methods=['POST'])
def analyze():
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    weather_condition = request.form['weather']
    throw_type = request.form['throw_type']
    video_file = request.files['video']

    # Save the video file
    video_path = os.path.join('uploads', session_id, video_file.filename)
    if not os.path.exists(os.path.dirname(video_path)):
        os.makedirs(os.path.dirname(video_path))
    video_file.save(video_path)

    # Upload video to Raspberry Pi
    ssh_upload_file(video_path, os.path.join(REMOTE_BASE_PATH, 'uploads', session_id, video_file.filename))

    # Extract frames and upload to Raspberry Pi
    frame_count = extract_frames_and_upload(video_path, session_id)

    # Delete local video after uploading
    os.remove(video_path)

    # Summarize the analysis of frames
    summary = summarize_analysis(frame_count, session_id)

    # Create a prompt for the AI to analyze the throw
    prompt = f"Analyze this ultimate frisbee throw. Consider the weather condition: {weather_condition} and throw type: {throw_type}. Describe any issues with the form and provide suggestions for improvement, but do so in a kind coach-like manner, be encouraging, and format your answer within 112 words, and make sure the answer is very nice, no weird formatting. Answer as if you've actually seen this user complete their throw"

    # Get feedback from GPT-4
    feedback = get_feedback_from_gpt4(prompt)

    # Cleanup: Remove the session folder and its contents
    local_frames_path = os.path.join('frames', session_id)
    if os.path.exists(local_frames_path):
        shutil.rmtree(local_frames_path)

    # Also, if needed, remove the session folder in 'uploads'
    session_upload_path = os.path.dirname(video_path)
    if os.path.exists(session_upload_path):
        shutil.rmtree(session_upload_path)

    return jsonify({"feedback": feedback})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
