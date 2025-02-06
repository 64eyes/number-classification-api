from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def is_prime(n):
    """Check if a number is prime (works for negatives)."""
    if n <= 1:
        return False
    n = abs(n)  # Handle negative numbers
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    """Check if a number is perfect (works for negatives)."""
    if n <= 1:
        return False
    n = abs(n)  # Handle negative numbers
    sum_divisors = 1
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            sum_divisors += i + n // i
    return sum_divisors == n

def is_armstrong(n):
    """Check if a number is an Armstrong number (handles negatives)."""
    if n <= 1:
        return False
    num = abs(n)  # Handle negative numbers
    digits = list(str(num))
    length = len(digits)
    total = sum(int(d) ** length for d in digits)
    return total == num

def digit_sum(n):
    """Calculate sum of digits (works for negatives)."""
    return sum(int(d) for d in str(abs(n)))

def fetch_fun_fact(n):
    """Fetch fun fact from NumbersAPI (handles negatives/errors)."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math")
        if response.status_code == 200:
            return response.text
        return f"{abs(n)} is a number that starts with a digit."  # Fallback
    except Exception as e:
        app.logger.error(f"Error fetching fun fact: {e}")
        return "No fun fact available."

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
    app.run(host='0.0.0.0', port=5000, debug=True)
