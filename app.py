from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/prediksi', methods=['GET', 'POST'])
def prediksi():
    input_names = [f'p{i}' for i in range(1, 16)]

    if request.method == 'POST':
        input_values = {}
        for name in input_names:
            if name == 'p5':
                input_values[name] = request.form.getlist('p5[]')
            else:
                value = request.form.get(name)
                try:
                    input_values[name] = float(value)
                except (ValueError, TypeError):
                    input_values[name] = None

        print("Data dari frontend:", input_values)
    return render_template("prediksi.html")



if __name__ == "__main__":
    app.run(debug=True)
