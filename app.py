from flask import Flask, jsonify, render_template, redirect, url_for, request
import requests

app = Flask(__name__)

def get_ip_info(ip=None):
    """Getting IP Information"""
    try:
        api_url = f"https://ipapi.co/{ip}/json/" if ip else "https://ipapi.co/json/"
        response = requests.get(api_url)
        
        # Print the response content for debugging
        print("API Response:", response.text)

        # Check for a successful response
        if response.status_code != 200:
            return {"error": "Unable to fetch IP information."}

        try:
            data = response.json()
        except ValueError:
            return {"error": "Invalid JSON response from API."}

        # Check if the response contains an error
        if data.get("error"):
            if data.get("reason") == "Reserved IP Address":
                # If there's an error and it's a reserved IP, handle accordingly
                return {
                    "ipv4": None if data.get('version') == "IPv4" else None,
                    "ipv6": data.get("ip") if data.get('version') == "IPv6" else None,
                    "country": "Reserved",
                    "country_code": None,
                    "region": "Reserved",
                    "city": "Reserved",
                    "provider": "Reserved",
                    "asn": "Reserved",
                    "latitude": "Reserved",
                    "longitude": "Reserved",
                }
            else:
                return {"error": data.get("reason")}

        # If the response is successful, extract IP information
        ip_info = {
            "ipv4": data.get("ip") if data.get('version') == "IPv4" else None,
            "ipv6": data.get("ip") if data.get('version') == "IPv6" else None,
            "country": data.get("country_name"),
            "country_code": data.get("country_code"),
            "region": data.get("region"),
            "city": data.get("city"),
            "provider": data.get("org"),
            "asn": data.get("asn"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
        }

        return ip_info

    except Exception as e:
        return {"error": str(e)}

@app.route('/get-ip-info', methods=['GET'])
def ip_info_route():
    # Get the IP address from the query parameter
    ip = request.args.get('ip')
    # Call Get IP Info function
    ip_info = get_ip_info(ip)
    return jsonify(ip_info)

@app.route('/')
def index():
    """Redirect to get ip page"""
    return redirect(url_for('show_get_ip_page'))

@app.route('/get-ip-page', methods=['GET'])
def show_get_ip_page():
    """Serve the frontend"""
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=8080)

    
