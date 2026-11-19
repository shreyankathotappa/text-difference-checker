
from flask import Flask, request, jsonify, render_template
import difflib

app = Flask(__name__)


# Compare two texts line by line
def compare_text(original, modified):
    original_lines = original.splitlines()
    modified_lines = modified.splitlines()

    differences = difflib.ndiff(original_lines, modified_lines)

    return list(differences)


# Homepage
@app.route("/")
def home():
    return render_template("index.html")


# API endpoint for comparing text
@app.route("/compare", methods=["POST"])
def compare():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON input"}), 400

    original = data.get("original")
    modified = data.get("modified")

    if not isinstance(original, str) or not isinstance(modified, str):
        return jsonify({"error": "Both texts must be strings"}), 400

    differences = compare_text(original, modified)

    return jsonify({"differences": differences}), 200


# Health check endpoint
@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)