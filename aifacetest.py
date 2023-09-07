from flask import Flask, render_template_string, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import random

app = Flask(__name__)

@app.route('/')
def show_images():
    

   
        
    local_image_filename = random.choice(os.listdir("static"))
    local_image_path = url_for('static', filename=local_image_filename)
    web_image_url = "https://thispersondoesnotexist.com"
    
    images = [
        {"id": "local_image", "src": local_image_path, "callback": "displayMessage('success')"},
        {"id": "web_image", "src": web_image_url, "callback": "displayMessage('failure')"}
    ]
    random.shuffle(images)

    return render_template_string("""
        <html>
            <head>
                <title>EY AI Image Guessing Game</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        text-align: center;
                        margin-top: 50px;
                    }
                    .image-container {
                        display: flex;
                        justify-content: center;
                    }
                    img {
                        margin: 10px 50px;  /* Increasing space between images */
                        width: 400px;
                        height: 400px;
                        cursor: pointer;
                    }
                    #message {
                        font-size: 24px;   /* Make the message font larger */
                        font-weight: bold; /* Bold the message */
                        margin: 20px 0;
                        color: blue;       /* Add color to the message */
                    }
                    #playAgainButton {
                        display: block;    /* Make the button a block element to center it */
                        margin: 20px auto; /* Center the button horizontally */
                        padding: 10px 20px;
                        font-size: 16px;
                        border: none;
                        border-radius: 5px;
                        background-color: #4CAF50;
                        color: white;
                        cursor: pointer;
                    }
                    #playAgainButton:hover {
                        background-color: #45a049;
                    }
                </style>
            </head>
            <body>
                <h1>Welcome to the EY AI Image Guessing Game!</h1>
                <p>Guess which image is AI Generated and which is real. Click on an image to make your choice.</p>
                <div class="image-container">
                    <img id="{{ images[0].id }}" src="{{ images[0].src }}" alt="Image 1" onclick="{{ images[0].callback }}">
                    <img id="{{ images[1].id }}" src="{{ images[1].src }}" alt="Image 2" onclick="{{ images[1].callback }}">
                </div>
                <div id="message"></div>
                <button id="playAgainButton" style="display: none;" onclick="location.reload();">Play Again</button>
                
                <script>
                    function displayMessage(type) {
                        const messageDiv = document.getElementById('message');
                        const playAgainButton = document.getElementById('playAgainButton');
                        const localImage = document.getElementById('local_image');
                        const webImage = document.getElementById('web_image');
                        
                        localImage.onclick = null;
                        webImage.onclick = null;

                        if (type === 'success') {
                            messageDiv.textContent = 'Success!';
                            messageDiv.style.color = 'green';
                        } else {
                            messageDiv.textContent = 'Not successful.';
                            messageDiv.style.color = 'red';
                        }

                        // Highlight the correct image always in green
                        localImage.style.border = "5px solid green";
                        webImage.style.border = "5px solid red";

                        playAgainButton.style.display = 'block';

                        
                            }
                        });
                    }
                </script>
            </body>
        </html>
    """, images=images)

if __name__ == "__main__":
    app.run(port=8080)
