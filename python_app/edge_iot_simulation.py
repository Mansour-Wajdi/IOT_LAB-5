from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated function for processing sensor data
def process_sensor_data(data):
    # Example: calculate the average of sensor values
    sensor_values = data.get("values", [])
    if not sensor_values:
        return {"error": "No sensor values provided"}

    avg_value = sum(sensor_values) / len(sensor_values)
    return {"average": avg_value, "status": "processed"}

@app.route('/process', methods=['POST'])
def process():
    # Get JSON data from the request
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400

        # Process the data
        result = process_sensor_data(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("\n--- Edge IoT Simulation App is running ---\n")
    print("Visit http://localhost:5000/process to interact with the app.\n")
    
    # Start the Flask app
    app.run(host="0.0.0.0", port=5000, debug=False)
