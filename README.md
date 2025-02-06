# Number Classification API

A Flask-based API that classifies numbers and returns their mathematical properties, including whether they are prime, perfect, or Armstrong numbers, along with a fun fact from the Numbers API.

---

## **Features**
- **Number Classification**: Determines if a number is prime, perfect, or an Armstrong number.
- **Digit Sum**: Calculates the sum of the digits of the number.
- **Fun Fact**: Fetches an interesting mathematical fact about the number from the Numbers API.
- **CORS Support**: Handles Cross-Origin Resource Sharing (CORS) for frontend integration.

---

## **API Endpoint**
### **GET `/api/classify-number`**
Classifies a number and returns its properties.

#### **Parameters**
- `number` (required): The number to classify. Must be an integer.

#### **Example Request**
```bash
curl http://3.86.101.92/api/classify-number?number=371
#### **Example Response (200 OK)**
json
Copy
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371."
}
Example Response (400 Bad Request)
json
Copy
{
    "number": "abc",
    "error": true
}
Deployment
This API is deployed on AWS EC2 using NGINX as a reverse proxy and Gunicorn as the WSGI server.

Steps to Deploy
Launch an EC2 Instance:

Use Ubuntu 22.04 LTS.

Open ports 80 (HTTP) and 22 (SSH) in the security group.

Install Dependencies:

bash
Copy
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx -y
Set Up the Project:

bash
Copy
git clone https://github.com/64eyes/number-classification-api.git
cd number-classification-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Configure Gunicorn:

Create a systemd service file (/etc/systemd/system/flask-api.service):

ini
Copy
[Unit]
Description=Gunicorn instance for Flask API
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/number-classification-api
Environment="PATH=/home/ubuntu/number-classification-api/venv/bin"
ExecStart=/home/ubuntu/number-classification-api/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
Start and enable the service:

bash
Copy
sudo systemctl daemon-reload
sudo systemctl start flask-api
sudo systemctl enable flask-api
Configure NGINX:

Create an NGINX config file (/etc/nginx/sites-available/flask-api):

nginx
Copy
server {
    listen 80;
    server_name 3.86.101.92;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
Enable the config and restart NGINX:

bash
Copy
sudo ln -s /etc/nginx/sites-available/flask-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
Test the API:

bash
Copy
curl http://3.86.101.92/api/classify-number?number=371
Dependencies
Python 3.8+

Flask

Gunicorn

NGINX

Requests

Install dependencies with:

bash
Copy
pip install -r requirements.txt
Contributing
Fork the repository.

Create a new branch (git checkout -b feature-branch).

Commit your changes (git commit -m "Add new feature").

Push to the branch (git push origin feature-branch).

Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Numbers API for providing fun facts.

Flask for the web framework.

AWS EC2 for hosting the API.
