from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import requests

app = Flask(__name__)

def extract_skin_color(image_path):
    # Function to extract skin color using OpenCV
    image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define skin color range in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    mask = cv2.inRange(hsv_image, lower_skin, upper_skin)
    
    # Calculate the average color of the skin area
    skin = cv2.bitwise_and(image, image, mask=mask)
    skin_color = cv2.mean(skin, mask=mask)[:3]
    
    return skin_color

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    # Extract skin color (for testing, replace with actual image path)
    image_path = 'path_to_your_image.jpg'
    skin_color = extract_skin_color(image_path)
    
    # Get recommendation type from frontend request
    request_data = request.json
    recommendation_type = request_data.get('type', 'jewellery')  # Default to jewellery
    
    # Define prompts based on recommendation type
    prompts = {
        'jewellery': 'Recommend the best type of jewellery according to this skin tone.',
        'outfit': 'Recommend the best colors for outfit suited for this skin tone.',
        'makeup': 'Which kind of makeup is suited best for this skin tone?'
    }
    
    prompt = prompts.get(recommendation_type, 'No valid recommendation type found.')
    
    # Prepare request payload for Gemini API
    gemini_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=YOUR_API_KEY'
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    # Send request to Gemini API
    response = requests.post(gemini_url, json=payload)
    
    if response.status_code == 200:
        generated_content = response.json().get('contents', [])
        recommendations = generated_content[0]['parts'][0]['text'] if generated_content else 'No recommendations found.'
        return jsonify({'skin_color': skin_color, 'recommendations': recommendations})
    else:
        return jsonify({'error': 'Error fetching recommendations from Gemini API'})

if __name__ == '__main__':
    app.run(debug=True)
