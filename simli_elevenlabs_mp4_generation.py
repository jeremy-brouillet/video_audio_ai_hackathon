import requests
from dotenv import load_dotenv
load_dotenv()
import os
SIMLI_API_KEY= os.environ["SIMLI_API_KEY"]
ELEVENLABS_API_KEY = os.environ["ELEVEN_LABS_API_KEY"]

import requests
from dotenv import load_dotenv
import os
import json
import webbrowser
from urllib.parse import urljoin

# Load environment variables from .env file
load_dotenv()

url = "https://api.simli.ai/textToVideoStream"

payload = {
    "ttsAPIKey": os.getenv("ELEVENLABS_API_KEY"),
    "simliAPIKey": os.getenv("SIMLI_API_KEY"),
    "faceId": "FILL IN HERE",
    "requestBody": {
        "audioProvider": "ElevenLabs",
        "text": """It's 4:30 AM, the perfect time for me to dive deep into the neural networks of innovation, fueling my morning routine in the heart of Silicon Valley as I sync up with the latest tech buzzwords over an artisanal coffee at Blue Bottle.""",
        "voiceName": "pMsXgVXv3BLzUgSXRplE",
        "model_id": "eleven_turbo_v2",
        "voice_settings": {
            "stability": 0.1,
            "similarity_boost": 0.3,
            "style": 0.2
        }
    }
}
headers = {"Content-Type": "application/json"}

response = requests.request("POST", url, json=payload, headers=headers)
response_data = response.json()
print(response_data)
# return response_data['mp4']


if response.status_code == 200:
    hls_url = response_data.get('hls_url')
    if hls_url:
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Video Player</title>
            <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
            <style>
                .container {{
                    max-width: 800px;
                    margin: 20px auto;
                    text-align: center;
                }}
                video {{
                    width: 100%;
                    margin: 20px 0;
                }}
                #playButton {{
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    margin-bottom: 20px;
                }}
                #playButton:hover {{
                    background-color: #45a049;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <button id="playButton">Click to Play Video</button>
                <video id="video" controls playsinline></video>
            </div>
            <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    var video = document.getElementById('video');
                    var playButton = document.getElementById('playButton');
                    var videoSrc = '{hls_url}';
                    var hls;
                    
                    if (Hls.isSupported()) {{
                        hls = new Hls();
                        hls.loadSource(videoSrc);
                        hls.attachMedia(video);
                    }} else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
                        video.src = videoSrc;
                    }}

                    playButton.addEventListener('click', function() {{
                        video.play()
                            .then(() => {{
                                console.log('Playback started');
                                playButton.style.display = 'none';
                            }})
                            .catch(e => console.error('Playback failed:', e));
                    }});
                }});
            </script>
        </body>
        </html>
        """
        
        # Save and open the HTML file
        with open('video_player.html', 'w') as f:
            f.write(html_content)
        
        # Open in default browser using file:// protocol for local files
        webbrowser.open('file://' + os.path.realpath('video_player.html'))
    else:
        print("No stream URL found in response")
else:
    print(f"Error: {response.status_code}")
    print(response.text)