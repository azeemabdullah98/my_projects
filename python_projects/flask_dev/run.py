from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'thisissecretkey'

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,nullable=False, unique=True)
    phone = db.Column(db.Integer,nullable=False, unique=True)
    password = db.Column(db.String,nullable=False)
    beneficiary = db.relationship('Beneficiary',backref="insurer",lazy=True)

class Beneficiary(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    fullname = db.Column(db.String,nullable=False,unique=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    id_card = db.Column(db.Integer,nullable=False,unique=True)
    gender = db.Column(db.String,nullable=False,default='Male')
    year_of_birth = db.Column(db.Integer,nullable=False)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({"message":"Token is missing!"}), 401

        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({"message":"Invalid token or expired!"}), 400
        
        return f(current_user, *args, **kwargs)
    return decorated


@app.route("/api/create",methods=['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'],method="sha256")

    user = User(username=data['username'],phone=data['phone'],password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message":"User successfully created!!"})

@app.route("/api/login")
def login_user():
    auth = request.authorization

    user = User.query.filter_by(username=auth['username']).first()

    if user.username != None and check_password_hash(user.password,auth['password']):
        token = jwt.encode({"user_id":user.id,"exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
        return jsonify({"status":200,
                        "JWT":token.decode('UTF-8')})
    return make_response("could not verify", 401, {'WWW-Authenticate':'Basic realm="Username or Password is Incorrect!"'})

@app.route("/api/beneficiary/add",methods=['POST'])
@token_required
def add_beneficiary(current_user):
    data = request.get_json()

    if data['id_card'] not in range(8000,10000):
        return jsonify({"message":"ID_Card already added to the beneficiary"}), 400
    
    beneficiary = Beneficiary(fullname=data['fullname'],user_id=current_user.id,id_card=data['id_card'],gender=data['gender'],year_of_birth=data['year_of_birth'])
    db.session.add(beneficiary)
    db.session.commit()
    return jsonify({"id":beneficiary.id,
                    "fullname":beneficiary.fullname,
                    "insurer_id":current_user.id,
                    "id_card":beneficiary.id_card,
                    "gender":beneficiary.gender,
                    "year_of_birth":beneficiary.year_of_birth})

@app.route("/api/beneficiary/delete/<int:_id>",methods=['DELETE'])
@token_required
def delete_beneficiary(current_user, _id):
    beneficiary = Beneficiary.query.filter_by(id=_id).first()

    if not beneficiary or beneficiary.insurer.id != current_user.id:
        return jsonify({"message":"bad request"}), 400

    db.session.delete(beneficiary)
    db.session.commit()
    return jsonify({}), 200
    


@app.route("/api/beneficiary",methods=['GET'])
@token_required
def get_beneficiary(current_user):
    beneficiary = Beneficiary.query.filter_by(user_id=current_user.id).all()
    output = []

    for b in beneficiary:
        data = {}
        data['id'] = b.id
        data['fullname'] = b.fullname
        data['id_card'] = b.id_card
        data['gender'] = b.gender
        data['year_of_birth'] = b.year_of_birth
        output.append(data)

    return output

@app.route("/api/beneficiary/<int:_id>")
@token_required
def get_one_beneficiary(current_user, _id):
    beneficiary = Beneficiary.query.filter_by(id=_id).first()

    if not beneficiary or beneficiary.insurer.id != current_user.id:
        return jsonify({"message":"bad request"}), 400


    data = {}
    data['id'] = beneficiary.id
    data['fullname'] = beneficiary.fullname
    data['id_card'] = beneficiary.id_card
    data['gender'] = beneficiary.gender
    data['year_of_birth'] = beneficiary.year_of_birth
    return data


if __name__ == "__main__":
    app.run(debug=True)