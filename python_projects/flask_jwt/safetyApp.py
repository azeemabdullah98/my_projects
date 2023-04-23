from flask import Flask, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
jwt = JWTManager(app)

app.app_context().push()

class UserModel(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    username = db.Column(db.String,unique=True)
    password = db.Column(db.String,nullable=False)
    mobile_number = db.Column(db.Integer,nullable=False)

class OfficerModel(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    officer_id = db.Column(db.Integer,unique=True)
    password = db.Column(db.String,nullable=False)
    phone_number = db.Column(db.Integer,nullable=False)

class ComplaintModel(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    title = db.Column(db.String,nullable=False,unique=True)
    description = db.Column(db.String,nullable=False)


@app.route("/user/login",methods=['POST','GET'])
def userLogin():
    data = request.get_json()

    if not data['username'] or not data['password']: #username and password of the user is required to login...
        return jsonify({"message":"bad credentials!"}), 401
    
    token = create_access_token({"username":data['username']})
    return jsonify({"token":token}), 200


@app.route("/officer/login",methods=['POST','GET'])
def officerLogin():
    data = request.get_json()

    if not data['officer_id'] or not data['password']: #officer_id and password of the officer is required to login...
        return jsonify({"message":"bad credentials!"}), 401
    
    token = create_access_token({"officer_id":data['officer_id']})
    return jsonify({"token":token}), 200

#route applicable only for the user...
@app.route("/complaint/register",methods=['POST','GET'])
@jwt_required()
def registerComplaint():
    current_user = get_jwt_identity()
    if current_user['username']:
        data = request.get_json()
        if not data['title'] or not data['description']:
            return jsonify({"message":"please fill the title/description"})
        complaint = ComplaintModel(title=data['title'],description=data['description'])
        db.session.add(complaint)
        db.session.commit()
        return jsonify({"message":"complaint successfully registered!"}), 200
    else:
        return jsonify({"message":"bad request"}), 401

@app.route("/criminal/records/",methods=['GET','POST'])
@jwt_required()
def accessCriminalRecords():
    current_user = get_jwt_identity()
    if current_user['officer_id']:
        complaints = ComplaintModel.query.all()
        output = []
        for complaint in complaints:
            res = {}
            res['title'] = complaint.title
            res['description'] = complaint.description

            output.append(res)
        return jsonify({"complaints":output}), 200
    else:
        return jsonify({"message":"bad request"}), 401

if __name__ == "__main__":
    app.run(debug=True)