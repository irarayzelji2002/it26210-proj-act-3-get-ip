from flask import Flask, jsonify, render_template, redirect, url_for, request
from flask_cors import CORS
import requests

app = Flask(__name__)
cors = CORS(app, origins="*")

IPQS_API_KEY = "D8LyW5f11ItL1azaN2GIZAHZFuNL3ryh"

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

def get_ip_reputation(ip=None):
    if not ip:
        return {"error": "IP address is required"}

    # Make API call to IPQualityScore
    api_url = f"https://ipqualityscore.com/api/json/ip/{IPQS_API_KEY}/{ip}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise HTTP errors
        data = response.json()
        
        if not data.get("success"):
            return {"error": data.get("message")}
        
        # Parse and return relevant fields
        return {
            "hostname": data.get("host"),
            "isp": data.get("ISP"),
            "organization": data.get("organization"),
            "zip_code": data.get("zip_code"),
            "asn": data.get("asn"),
            "timezone": data.get("timezone"),
            "fraud_score": data.get("fraud_score"),
            "is_crawler": data.get("is_crawler"),
            "is_proxy": data.get("proxy"),
            "is_vpn": data.get("vpn"),
            "is_active_vpn": data.get("active_vpn"),
            "is_tor": data.get("tor"),
            "is_active_tor": data.get("active_tor"),
            "is_mobile": data.get("mobile"),
            "recent_abuse": data.get("recent_abuse"),
            "bot_status": data.get("bot_status"),
            "connection_type": data.get("connection_type"), # Premium required.
            "abuse_velocity": data.get("abuse_velocity"),   # Premium required.
        }
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.route('/get-ip-info', methods=['GET'])
def ip_info_route():
    # Get the IP address from the query parameter
    ip = request.args.get('ip')
    if not ip:
        return jsonify({"error": "IP address is required."}), 400

    # Fetch IP info
    ip_info = get_ip_info(ip)
    if "error" in ip_info and isinstance(ip_info["error"], str):
        return jsonify({"ip_info": ip_info, "ip_reputation": {"error": "Skipped due to IP info error"}}), 200

    # Fetch IP reputation
    ip_reputation = get_ip_reputation(ip)
    if "error" in ip_reputation and isinstance(ip_reputation["error"], str):
        return jsonify({"ip_info": ip_info, "ip_reputation": ip_reputation}), 200

    # Combine the results if no errors
    combined_data = {
        "ip_info": ip_info,
        "ip_reputation": ip_reputation,
    }
    return jsonify(combined_data)

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

    
