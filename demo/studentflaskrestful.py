import json
import pymongo
from flask import Flask,  request
from flask_restful import Resource, Api


client=pymongo.MongoClient("mongodb+srv://mongouser:mongopwd@cluster1.davwpcs.mongodb.net/?retryWrites=true&w=majority")
datalist=client["mydatabase"]
col=datalist["resigtry"]

app=Flask(__name__)

api = Api(app)

class Student(Resource):

    def get(self):
        try:
          
            x= col.find_one()
            print(type(x))
                
            return x
        except Exception as e:
            print("error on get_stu_details :" +str(e))

    
    def post(self):
        try:
            stu=request.get_json()
            col.insert_one(stu)
            return "Successfully added"

        except Exception as e:
            print("error on get_stu_details :" +str(e))


    
    def delete():
        try:
            Rno = request.get_json()
            col.delete_one(Rno)
            return "deleted successfully"
        
        except Exception as e:
            print("error"+str(e))


    
    def put():
        try:
            Rno = request.args.get("Rno")
            data=request.get_json()
            col.find_one_and_update({"Rno":Rno},{"$set":data})
            return "success"



        except Exception as e:
            print("error on updation :" +str(e))

api.add_resource(Student, '/')


if __name__=='__main__':
    app.run(debug=True)
