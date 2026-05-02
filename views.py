import requests

def validate_turnstile(token, secret, remoteip=None):
    url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'

    data = {
        'secret': secret,
        'response': token
    }

    if remoteip:
        data['remoteip'] = remoteip

    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Turnstile validation error: {e}")
        return {'success': False, 'error-codes': ['internal-error']}

# Usage with Flask
from flask import Flask, request, jsonify

app = Flask(__name__)
SECRET_KEY = '0x4AAAAAADHRPsz7BGrK-U0Sd2ConCficI8'

@app.route('/submit-form', methods=['POST'])
def submit_form():
    token = request.form.get('cf-turnstile-response')
    remoteip = request.headers.get('CF-Connecting-IP') or \
               request.headers.get('X-Forwarded-For') or \
               request.remote_addr

    validation = validate_turnstile(token, SECRET_KEY, remoteip)

    if validation['success']:
        # Valid token - process form
        return jsonify({'status': 'success', 'message': 'Form submitted successfully'})
    else:
        # Invalid token - reject submission
        return jsonify({
            'status': 'error',
            'message': 'Verification failed',
            'errors': validation['error-codes']
        }), 400
