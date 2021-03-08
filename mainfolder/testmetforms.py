from flask import Flask, render_template, request
from eerstebototest import listalleinstances,customkeylistalleinstances
from eerstebototest import alleregios



from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('requestform.html')

@app.route('/', methods=['POST','GET'])
def my_form_post():
    text = request.form['acceskey']
    text2 = request.form['accesspw']
    processed_text = text.upper()+text2
    lijstvanregios=(request.form.getlist('regiocheckbox'))
    processed_text2= text.upper
    if 'all' in lijstvanregios:
        print('all zit in de lijst')
        regios = alleregios()
    else:
        regios=lijstvanregios

    lijstvoorinstanceinformatie = customkeylistalleinstances(regios,text,text2)
    #print(lijstvoorinstanceinformatie)
    return render_template("tweeinformatie.html", len = len(lijstvoorinstanceinformatie), lijstvoorinstanceinformatie = lijstvoorinstanceinformatie)


if __name__ == "__main__":
    app.run(debug=True)