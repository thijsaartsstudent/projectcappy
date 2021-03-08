from flask import Flask, render_template,request
from eerstebototest import listalleinstances,customkeylistalleinstances,securitygroupdef,prinformation,alleregios
from tweedebototest import customkeylistalleinstances2

app = Flask(__name__)

#regios=alleregios()
regios=['us-east-1','us-east-2','us-west-1','us-west-2','af-south-1','ap-east-1','ap-south-1','ap-northeast-1','ap-northeast-2','ap-southeast-1','ap-southeast-2','ca-central-1','eu-central-1','eu-west-1','eu-west-2','eu-west-3','eu-south-1','eu-north-1','me-south-1','sa-east-1']
lijstvoorinstanceinformatie=listalleinstances(regios)
#dit is een test voor gitpublishing


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/instancerequest")
def instancerequest():
    return render_template('instancerequest.html')

@app.route("/instancerequest", methods=['POST','GET'])
def my_form_post():
    values = request.form.getlist('input_text[]')
    print(values)
    tijdverschil=0
    meetperformanceon=0
    text = request.form['acceskey']
    text2 = request.form['accesspw']
    text3 = request.form['opacceskey']
    text4 = request.form['opaccesspw']

    lijstvanregios=(request.form.getlist('regiocheckbox'))
    lijstvanprojectop = (request.form.getlist('input_text[]'))
    lijstvanprojectop2 = (request.form.getlist('field_name2[]'))
    print(lijstvanprojectop2)
    #lijstvanprojectop = request.form.getlist('input_text[]')
    print(text,text2)
    print('lijst van projects')
    print('dit is de nieuwe lijst',lijstvanprojectop)
    processed_text2= text.upper
    if request.form.get('enableperformance'):
        meetperformanceon= 1
        tijdverschil = request.form['options']

    if 'all' in lijstvanregios:
        print('all zit in de lijst')
        regios = alleregios(text,text2)
    else:
        regios=lijstvanregios
        print(lijstvanregios)


    devvoorinstanceinformatie = customkeylistalleinstances2(regios,text,text2,meetperformanceon,tijdverschil)
    if not devvoorinstanceinformatie:
        return render_template('verkeerdeaccesskey.html')
    #devvoorinstanceinformatie={'eu-west-2': {'vpc': {'vpc-04ce29592baff31ea': {'address': '172.31.0.0/16'}}, 'elasticip': {'54.155.235.250': {'associated': 'no'}, '54.75.186.9': {'associated': 'i-0fa6ec3c1e3909de5'}}, 'gatewayid': {'igw-07e6f988084650259': {'gatewaystate': 'available', 'intergatewayvpcid': 'vpc-04ce29592baff31ea'}}}, 'eu-west-1': {'vpc': {'vpc-07d99d243ac4efaca': {'address': '10.0.0.0/16', 'i-0fa6ec3c1e3909de5': {'instancetype': 't2.micro', 'status': 'stopped'}, 'i-084e84a7fcdf50b18': {'instancetype': 't2.micro', 'status': 'stopped'}}}, 'elasticip': {'54.155.235.250': {'associated': 'no'}, '54.75.186.9': {'associated': 'i-0fa6ec3c1e3909de5'}}, 'gatewayid': {'igw-0274f0745a806c219': {'gatewaystate': 'available', 'intergatewayvpcid': 'vpc-07d99d243ac4efaca'}, 'igw-0828ee9999180adf1': {'intergatewayvpcid': 'hij is niet attached'}}}, 'us-east-2': {'vpc': {'vpc-057b22e7dc595c4fe': {'address': '172.31.0.0/16'}}, 'elasticip': {}, 'gatewayid': {'igw-08d830bd2d131b8e8': {'gatewaystate': 'available', 'intergatewayvpcid': 'vpc-057b22e7dc595c4fe'}}}, 'us-west-1': {'vpc': {'vpc-08c7987f7a4dec891': {'address': '172.31.0.0/16', 'i-0b1801827f4b5f167': {'instancetype': 't2.micro', 'status': 'stopped'}}}, 'elasticip': {}, 'gatewayid': {'igw-02e99cbec385ae33e': {'gatewaystate': 'available', 'intergatewayvpcid': 'vpc-08c7987f7a4dec891'}}}, 'us-west-2': {'vpc': {'vpc-0c02b082434b5560e': {'address': '172.31.0.0/16'}}, 'elasticip': {}, 'gatewayid': {'igw-0e71c23ac44a49176': {'gatewaystate': 'available', 'intergatewayvpcid': 'vpc-0c02b082434b5560e'}}}}
    print('dit is de lijst van instanceinformatie',lijstvoorinstanceinformatie)
    return render_template("instanceinformatie.html", len = len(devvoorinstanceinformatie), devvoorinstanceinformatie = devvoorinstanceinformatie)

@app.route("/securityrequest")
def securityrequest():
    return render_template('securityrequest.html')

@app.route("/securityrequest", methods=['POST','GET'])
def securityinformatie():
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
        print(lijstvanregios)

    lijstvoorsecurityinformatie = securitygroupdef(regios,text,text2)
    #lijstvoorsecurityinformatie = ['eu-west-2', ['sg-0bf91dd38cb7592dd', ['je hebt alle porten open']], 'eu-west-1', ['sg-07a20d94e4aa7e988', ['je hebt de ssh port openstaan en iedereen kan erbij'], 'sg-09cfdc37ee1cc12f5', ['je hebt de ssh port openstaan en iedereen kan erbij', 'je hebt de ssh port openstaan en iedereen kan erbij'], 'sg-0c971f51ea5349fc0', ['je hebt de ssh port openstaan en iedereen kan erbij'], 'sg-0d76bb70a15bb6e3e', ['je hebt alle porten open'], 'sg-0e6d1fb3fd4379abd', ['je hebt de ssh port openstaan en iedereen kan erbij']], 'us-east-2', ['sg-082c29bb2634e0899', ['je hebt alle porten open']], 'us-west-1', ['sg-011a1be4cd070173c', ['je hebt de ssh port openstaan en iedereen kan erbij'], 'sg-0c17c80f13bbeb070', ['je hebt alle porten open'], 'sg-0d1a8a361826fa543', ['je hebt de ssh port openstaan en iedereen kan erbij']], 'us-west-2', ['sg-0b14d3c4bc6a65896', ['je hebt alle porten open']]]


    #regiolist,grouplist,infolist=prinformation
    #print('dit is de lijst van instanceinformatie',lijstvoorinstanceinformatie)

    return render_template("securityinformatie.html", lijstvoorsecurityinformatie = lijstvoorsecurityinformatie,)

if __name__ == "__main__":
    app.run(debug=True)