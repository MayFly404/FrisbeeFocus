import os
from flask import Flask, render_template, request, jsonify
import openai
import cv2

app = Flask(__name__)

# 0.tcp.ngrok.io:14534

# Ensure the 'uploads' directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Set your OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_frames(video_path, output_folder='frames'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0

    while success:
        frame_path = os.path.join(output_folder, f"frame{count}.jpg")
        cv2.imwrite(frame_path, image)
        success, image = vidcap.read()
        count += 1

    vidcap.release()
    return count, output_folder

def analyze_frame(frame_path):
    # Placeholder function for frame analysis
    # Implement your own analysis logic here
    return "Frisbee detected in frame. Throw angle looks good."

def summarize_analysis(frame_folder, frame_count):
    summaries = []
    for i in range(frame_count):
        frame_path = os.path.join(frame_folder, f"frame{i}.jpg")
        summary = analyze_frame(frame_path)
        summaries.append(summary)
    return " ".join(summaries)

def get_feedback_from_gpt4(summary):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
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

@app.route('/analyze', methods=['POST'])
def analyze():
    weather_condition = request.form['weather']
    throw_type = request.form['throw_type']
    video_file = request.files['video']

    # Save the video file
    video_path = os.path.join('uploads', video_file.filename)
    video_file.save(video_path)

    # Extract frames from video
    frame_count, frame_folder = extract_frames(video_path)

    # Summarize the analysis of frames
    summary = summarize_analysis(frame_folder, frame_count)

    # Create a prompt for the AI to analyze the throw
    prompt = f"Analyze this ultimate frisbee throw. Consider the weather condition: {weather_condition} and throw type: {throw_type}.Describe any issues with the form and provide suggestions for improvement, but do so in a kind coach like manner, be encouraging, and format your answer within 112 words, and make sure the answer is very nice, no weird formatting. Answer as if you've actually seen this user complete their throw"

    # Get feedback from GPT-4
    feedback = get_feedback_from_gpt4(prompt)

    return jsonify({"feedback": feedback})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)