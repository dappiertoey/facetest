from flask import Flask, render_template_string, url_for
import os
import random

app = Flask(__name__)

@app.route('/')
def show_images():
    # Get a random image from the static folder
    local_image_filename = random.choice(os.listdir("test"))
    
    # Using Flask's url_for to generate the image path
    local_image_path = url_for('test', filename=local_image_filename)
    
    # Web image URL
    web_image_url = "https://thispersondoesnotexist.com"
    
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
                    <!-- Attach onclick events to the images -->
                    <img id="local_image" src="{{ local_image_path }}" alt="Local Image" onclick="displayMessage('success')">
                    <img id="web_image" src="{{ web_image_url }}" alt="Web Image" onclick="displayMessage('failure')">
                </div>
                <div id="message"></div> <!-- This div will display the success message -->
                <button id="playAgainButton" style="display: none;" onclick="location.reload();">Play Again</button>
                
                <script>
                    function displayMessage(type) {
                        const messageDiv = document.getElementById('message');
                        const playAgainButton = document.getElementById('playAgainButton');
                        const localImage = document.getElementById('local_image');
                        const webImage = document.getElementById('web_image');
                        
                        // Disable further image clicks
                        localImage.onclick = null;
                        webImage.onclick = null;

                        // Highlight correct and wrong images
                        if (type === 'success') {
                            messageDiv.textContent = 'Success!';
                            messageDiv.style.color = 'green';  /* Make the success message green */
                            localImage.style.border = "5px solid green";
                            webImage.style.border = "5px solid red";
                        } else {
                            messageDiv.textContent = 'Not successful.';
                            messageDiv.style.color = 'red';    /* Make the failure message red */
                            webImage.style.border = "5px solid green";
                            localImage.style.border = "5px solid red";
                        }

                        // Show play again button
                        playAgainButton.style.display = 'block';
                    }
                </script>
            </body>
        </html>
    """, local_image_path=local_image_path, web_image_url=web_image_url)

if __name__ == "__main__":
    app.run(port=8080)
