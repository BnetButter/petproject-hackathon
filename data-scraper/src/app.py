from flask import Flask, jsonify, send_from_directory, abort
import os
from datetime import datetime
import json

app = Flask(__name__)
BASE_DIR = '/app/data'

def get_latest_directory():
    try:
        directories = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))]
        latest_directory = max(directories, key=lambda d: datetime.strptime(d, '%Y-%m-%d'))
        return latest_directory
    except ValueError:
        return None

@app.route('/inspection-data/latest', methods=['GET'])
def latest_report():
    latest_directory = get_latest_directory()
    if not latest_directory:
        return jsonify({"error": "No directories found"}), 404

    report_path = os.path.join(BASE_DIR, latest_directory, 'report.geojson')
    if not os.path.exists(report_path):
        return jsonify({"error": "report.geojson not found in latest directory"}), 404

    with open(report_path) as f:
        geojson_data = f.read()

    return jsonify(json.loads(geojson_data))

@app.route('/inspection-data/files/<date>/<file>', methods=['GET'])
def download_file(date, file):
    directory_path = os.path.join(BASE_DIR, date)
    if not os.path.exists(directory_path):
        return abort(404)

    file_path = os.path.join(directory_path, file)
    if not os.path.exists(file_path):
        return abort(404)

    return send_from_directory(directory_path, file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
