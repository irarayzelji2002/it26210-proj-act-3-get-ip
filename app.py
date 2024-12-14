from flask import Flask, jsonify, render_template, redirect, url_for, request
from flask_cors import CORS
import requests

app = Flask(__name__)
cors = CORS(app, origins="*")

IPINFO_ACCESS_TOKEN = "3489102523e216"
IPQS_API_KEY = "D8LyW5f11ItL1azaN2GIZAHZFuNL3ryh"

def get_ip_info(ip=None):
    """Getting IP Information"""
    try:
        # Construct API URL
        api_url = f"https://ipinfo.io/{ip}/json?token={IPINFO_ACCESS_TOKEN}" if ip else f"https://ipinfo.io/json?token={IPINFO_ACCESS_TOKEN}"
        
        # Add the API token as a Bearer token in the headers
        headers = {"Authorization": f"Bearer {IPINFO_ACCESS_TOKEN}"}
        response = requests.get(api_url, headers=headers)

        # Print the response content for debugging
        print("API Response (IP Info):", response.text)

        # Check for a successful response
        if response.status_code != 200:
            return {"error": "Unable to fetch IP information."}

        try:
            data = response.json()
        except ValueError:
            return {"error": "Invalid JSON response from API."}
        
        # Check for bogon IP
        if data.get("bogon"):
            return {
                "ipv4": data.get("ip"),
                "ipv6": None,
                "country": None,
                "country_code": None,
                "region": None,
                "city": None,
                "provider": None,
                "asn": None,
                "latitude": None,
                "longitude": None,
                "note": "Minimal information returned for this IP address.",
            }
        
        # Check if the response contains only an IP
        if "ip" in data and len(data) == 1:
            return {
                "ipv4": None,
                "ipv6": data.get("ip"),
                "country": None,
                "country_code": None,
                "region": None,
                "city": None,
                "provider": None,
                "asn": None,
                "latitude": None,
                "longitude": None,
                "note": "Minimal information returned for this IP address.",
            }

        # Extract latitude and longitude from "loc" field
        location = data.get("loc", "").split(",")  # Split latitude and longitude
        latitude = location[0] if len(location) > 0 else None
        longitude = location[1] if len(location) > 1 else None
        
        # Extract ASN from the "org" field
        org_info = data.get("org", "")
        asn = org_info.split(" ")[0] if org_info.startswith("AS") else None
        org = " ".join(org_info.split(" ")[1:]) if asn else org_info

        # Prepare IP info
        ip_info = {
            "ipv4": data.get("ip"),
            "ipv6": None,  # ipinfo.io does not provide separate IPv6 field in free tier
            "country": data.get("country"),
            "country_code": data.get("country"),
            "region": data.get("region"),
            "city": data.get("city"),
            "provider": org,
            "asn": asn,
            "latitude": latitude,
            "longitude": longitude,
            "postal": data.get("postal"),
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
        
        # Print the response content for debugging
        print("API Response (IP Reputation):", response.text)
        
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

    # Fetch IP info
    ip_info = get_ip_info(ip)
    if "error" in ip_info and isinstance(ip_info["error"], str):
        return jsonify({"ip_info": ip_info, "ip_reputation": {"error": "Skipped due to IP info error"}}), 200

    # Fetch IP reputation
    ip_reputation = get_ip_reputation(ip_info.get("ipv4") or ip_info.get("ipv6"))
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

    
