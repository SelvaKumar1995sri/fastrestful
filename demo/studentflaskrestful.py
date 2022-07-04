import json
import pymongo
from flask import Flask,  request
from flask_restful import Resource, Api


client=pymongo.MongoClient("mongodb+srv://mongouser:mongopwd@cluster1.davwpcs.mongodb.net/?retryWrites=true&w=majority")
datalist=client["mydatabase"]
stu_col=datalist["registry"]
user_db=datalist["db"]

app=Flask(__name__)

api = Api(app)

def auth_api(func):
    def wrapper(*args,**kwargs):
        print("started")
        user_name=user_db.find({},{"name":1})
        for i in user_name:
            if request.headers.get("x-api-key")==i:
                resp=func(*args,**kwargs)           
            else:
                return "unauthorised user"

        print("stoped")
        return resp
        
    return wrapper

class Students(Resource):

    @auth_api
    def get(self):
        try:
          
            x= stu_col.find({},{"_id":0})
            
            return [i for i in x]
            
        except Exception as e:
            print("error on get_stu_details :" +str(e))

    @auth_api
    def post(self):
        try:
            stu=request.get_json()
            stu_col.insert_one(stu)
            return "Successfully added"

        except Exception as e:
            print("error on get_stu_details :" +str(e))


    @auth_api
    def delete(self):
        try:
            no = request.get_json()
            print(no)
            stu_col.delete_one({"Rno":no})
            return "deleted successfully"
        
        except Exception as e:
            print("error"+str(e))


    @auth_api
    def put(self):
        try:
            Rno = request.args.get("Rno")
            data=request.get_json()
            stu_col.find_one_and_update({"Rno":Rno},{"$set":data})
            return "success"



        except Exception as e:
            print("error on updation :" +str(e))

api.add_resource(Students, '/students')


if __name__=='__main__':
    app.run(debug=True)
