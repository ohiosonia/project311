from flask import jsonify 
from app import app
from cassandra.cluster import Cluster
from flask import render_template
from flask import Flask
from flask import request

cluster = Cluster(['172.31.0.134']) 
session = cluster.connect('playground')

# Change tabs
@app.route("/")
@app.route("/index")  
def index():
   title = "The 411 on the 311"
   return render_template("home.html", title = title)

@app.route('/zipcodeComplaints', methods=['GET','POST'])
def zipcodeComplaints():
    if request.method=="GET":
        return render_template('zipcodeComplaints.html')
    if request.method=="POST":
        response_list=[]

        if 'incident_zip' in request.form: 
           incident_zip = request.form['incident_zip']

    stmt = "SELECT * FROM zipcode_complaints WHERE incident_zip=%s"
    response = session.execute(stmt, parameters=[int(incident_zip)])
    for val in response:
       response_list.append(val)
    jsonresponse = [{"complaint_type": x.complaint_type, "incident_zip": x.incident_zip, "total":x.total} for x in response_list]
    return jsonify(data=jsonresponse)


