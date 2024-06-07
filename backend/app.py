from flask import Flask, jsonify, request, render_template
import numpy as np
from scipy.fft import fft, ifft
import sympy as sp

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/process_signal', methods=['POST'])
def process_signal():
    data = request.json
    equation = data.get('equation')
    processing_type = data.get('processing')

    if not equation or not processing_type:
        return jsonify(error="Equation or processing type not provided"), 400

    try:
        # Use sympy to safely parse the equation
        x = sp.symbols('x')
        expr = sp.sympify(equation)
        
        # Generate x values and signal from the evaluated expression
        x_vals = np.linspace(0, 2 * np.pi, 100)
        signal = np.array([expr.evalf(subs={x: val}) for val in x_vals], dtype=float)

        if processing_type == 'fourier_transform':
            processed_signal = fft(signal).tolist()
        elif processing_type == 'ifft':
            processed_signal = ifft(signal).tolist()
        else:
            return jsonify(error="Invalid processing type"), 400

        return jsonify(
            x_values=x_vals.tolist(),
            original_signal=signal.tolist(),
            processed_signal=processed_signal
        )

    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True)

