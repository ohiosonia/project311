
from flask import jsonify 
from app import app
from cassandra.cluster import Cluster
from flask import render_template

cluster = Cluster(['ec2-52-71-164-204.compute-1.amazonaws.com']) 
session = cluster.connect('playground')

@app.route('/')
@app.route('/index')
def index():
   user = { 'nickname': 'Miguel' } # fake user
   return render_template("index.html", title = 'Home')

@app.route('/api/<complaint>/')
def get_complaint_total(complaint):
        stmt = "SELECT * FROM complaints WHERE complaint_type=%s"
        response = session.execute(stmt, parameters=[complaint])
        response_list = []
        for val in response:
             response_list.append(val)
        jsonresponse = [{"complaint": x.complaint_type, "total complaints": x.total} for x in response_list]
        return jsonresponse

@app.route('/complaint')
def complaint():
 print "im here"
 json = get_complaint_total('<id>')
 return render_template("complaint.html", output=json)

@app.route("/complaint", methods=['POST'])
def email_post():
         emailid = request.form["complaint_type"] 
         date = request.form["total"]
         stmt = "SELECT * FROM complaints WHERE complaint_type=%s and total=%s"
         response = session.execute(stmt, parameters=[emailid, date])
         response_list = []
         for val in response:
              response_list.append(val)
         jsonresponse = [{"complaint_type": x.complaint_type, "total": x.total} for x in response_list]
         return render_template("emailop.html", output=jsonresponse)



