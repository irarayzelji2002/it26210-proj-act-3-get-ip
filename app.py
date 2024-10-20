from flask import Flask, jsonify, render_template, redirect, url_for
import requests

app = Flask(__name__)

# API endpoint for ipapi.co
api_url = "https://ipapi.co/json/"

def get_ip_info():
    """Getting IP Information"""
    try:
        response = requests.get(api_url)
        data = response.json()

        ipv4 = data.get("ip")
        ipv6 = data.get("ipv6")
        country = data.get("country_name")
        country_code = data.get("country_code")
        region = data.get("region")
        city = data.get("city")
        provider = data.get("org")
        asn = data.get("asn")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        ip_info = {
            "ipv4": ipv4,
            "ipv6": ipv6,
            "country": country,
            "country_code": country_code,
            "region": region,
            "city": city,
            "provider": provider,
            "asn": asn,
            "latitude": latitude,
            "longitude": longitude,
        }

        return ip_info

    except Exception as e:
        return {"error": str(e)}

@app.route('/get-ip-info', methods=['GET'])
def ip_info_route():
    ip_info = get_ip_info()
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

    
