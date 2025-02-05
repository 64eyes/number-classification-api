from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n <= 1:
        return False
    sum_divisors = 1
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            sum_divisors += i + n // i
    return sum_divisors == n

def is_armstrong(n):
    digits = list(str(n))
    length = len(digits)
    total = sum(int(d) ** length for d in digits)
    return total == n

def digit_sum(n):
    return sum(int(d) for d in str(abs(n)))

def fetch_fun_fact(n):
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math")
        return response.text if response.status_code == 200 else "No fun fact found."
    except:
        return "No fun fact found."

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_str = request.args.get('number')
    
    # Validate input
    if not number_str:
        return jsonify({"error": "Missing 'number' parameter"}), 400
    try:
        number = int(number_str)
    except ValueError:
        return jsonify({"number": number_str, "error": True}), 400
    
    # Determine properties
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    properties.append("even" if number % 2 == 0 else "odd")
    
    return jsonify({
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": fetch_fun_fact(number)
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
