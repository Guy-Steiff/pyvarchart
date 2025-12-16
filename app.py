from flask import Flask, request, jsonify, send_file, send_from_directory
import os
import pandas as pd
import uuid
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for servers

from pyvarchart_wrapper import run_pyvarchart

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


@app.route('/')
def home():
    return send_from_directory('static', 'index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        print("[DEBUG] /upload called")

        file = request.files.get('file')
        if not file:
            print("[ERROR] No file in request")
            return jsonify({'error': 'No file uploaded'}), 400

        ext = os.path.splitext(file.filename)[-1]
        file_id = str(uuid.uuid4())
        filename = f"{file_id}{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Try reading file just to get column names
        if ext.lower() in ['.xlsx', '.xls']:
            df = pd.read_excel(filepath)
        else:
            df = pd.read_csv(filepath)

        columns = df.columns.tolist()
        return jsonify({'file_id': file_id, 'columns': columns})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    file_id = data.get('file_id')
    config = data.get('config')

    if not file_id or not config:
        return jsonify({'error': 'Missing file_id or config'}), 400

    file_path = find_file_by_id(file_id)
    if not file_path:
        return jsonify({'error': 'File not found'}), 404

    try:
        if file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)
    except Exception as e:
        return jsonify({'error': f'Failed to read file: {str(e)}'}), 500

    try:
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{file_id}.png")
        run_pyvarchart(config, df, output_path)
        return jsonify({'image_url': f"/plot/{file_id}.png"})
    except Exception as e:
        return jsonify({'error': f'Failed to generate plot: {str(e)}'}), 500


@app.route('/plot/<filename>')
def get_plot(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), mimetype='image/png')

def find_file_by_id(file_id):
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        if file.startswith(file_id):
            return os.path.join(app.config['UPLOAD_FOLDER'], file)
    return None


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)  #, port=5050)
