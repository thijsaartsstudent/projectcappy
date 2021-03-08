from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/')
def search():
    return render_template('dynamic_input.html')

@app.route('/results', methods = ['GET', 'POST'])
def results():
    if request.method == 'GET':
        return redirect(url_for('/'))
    else:
        values = request.form.getlist('input_text[]')
        print(values)
        return render_template('dynamic_input_results.html',
                               values = values)

if __name__ == '__main__':
    app.run(debug = True)