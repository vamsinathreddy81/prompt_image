import openai
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

api_key = "ai key"
openai.api_key = api_key

html_input_form = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Generation</title>
    <style>
        body {
            background-image: url('OIP.jpeg');
            /* Replace 'background.jpg' with your image file */
            background-size: cover;
            height:100vh;
            color: white;
            font-family: 'Arial', sans-serif;
        }

        h1 {
            text-align: center;
        }

        form {
            width: 50%;
            margin: 0 auto;
            background: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
        }

        label, input, button {
            display: block;
            margin: 10px 0;
        }

        input {
            width: 100%;
            padding: 8px;
        }

        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Generate Image</h1>
    <form action="/generate_image" method="post">
        <label for="prompt">Enter Prompt:</label>
        <input type="text" id="prompt" name="prompt" required>
        <button type="submit">Generate Image</button>
    </form>
</body>
</html>
"""

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html_input_form.encode())
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        user_prompt = parse_qs(post_data)['prompt'][0]

        response = openai.Image.create(prompt=user_prompt, n=1, size="1024x1024")
        image_url = response['data'][0]['url']

        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Generated Image</title>
         
        </head>
        <body style="display:flex;align-items:center;justify-content:center;">
            <h1 style="font-weight:20px;">Generated Image   :</h1>
            <img style="background:black;" src="{image_url}" alt="Generated Image" width="500">
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html_template.encode())

webbrowser.open("http://localhost:8000")
HTTPServer(('', 8000), RequestHandler).serve_forever()
