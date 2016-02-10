from flask import jsonify 
from app import app
from cassandra.cluster import Cluster
from flask import render_template
from flask import Flask
from flask import request
import datetime
import re, time
from datetime import timedelta
from collections import OrderedDict

cluster = Cluster(['ec2-52-71-164-204.compute-1.amazonaws.com']) 
session = cluster.connect('playground')

# return list of zipcodes
def return_zipcodes() :
    # Declare variables
    response_list = []

    # Read line by line
    with open('/home/ubuntu/project311/kafka/zipcodes.txt', 'rU') as infile:
        for line in infile :
            response_list.append(line.strip()) # strip

    return response_list

# Change tabs
@app.route("/")
@app.route("/index")  
def index():
   title = "The 411 on the 311"
   return render_template("home.html", title = title)

@app.route("/aboutme")
def aboutme():
   title = "The 411 on the 311"
   return render_template("aboutme.html", title = title)

@app.route("/projectoverview")
def projectoverview():
   title = "The 411 on the 311"
   return render_template("aboutme.html", title = title)

@app.route('/liveview')
def liveview():
    return render_template("liveview.html")

@app.route("/currenttrends")
def history_zipcode_hourly_search():
    # Declare variables
    response_list = return_zipcodes()
    print response_list

    return render_template("currenttrends.html", response_list=response_list)


@app.route("/currenttrendsByZipcode", methods=['GET', 'POST'])
def currenttrendsByZipcode():
    print 'i m here'
    zipcode = request.form["zipcode"]
    print zipcode

    stmt = "SELECT zipcode, time, total FROM live_complaints2 WHERE zipcode = %s ALLOW FILTERING"
    response = session.execute(stmt, parameters=[zipcode])
   
    print response, type(response)
   # dt=datetime.datetime.strptime(str("event_time"),'%Y%m%d%H%M%S')
    tmp_dict = {}
    for val in response:
        print val
        print val.time
        date_string = val.time
      	date_time = datetime.datetime.strptime(str(date_string),'%Y%m%d%H%M%S')
	#epoch = date_time.total_seconds()
	epoch = (date_time - datetime.datetime(1970,1,1)).total_seconds()*1000
        #print date_time
	#print epoch
	tmp_dict[epoch] = val.total
    print tmp_dict, type(tmp_dict)
    keys = tmp_dict.keys()
    keys.sort()
    
    jsonresponse = []
    for key in keys:
        jsonresponse.append([key, tmp_dict[key]])
    print jsonresponse, type(jsonresponse)
    return render_template("currenttrendschart.html", zipcode=zipcode, jsonresponse=jsonresponse)

@app.route("/neighborhoodawards")
def neighborhoodawards():
#Animal Lovers ('Illegal Animal Kept as Pet')
   title = "The 411 on the 311"
   stmt = "SELECT * FROM awards WHERE complaint_type = 'Illegal Animal Kept as Pet' limit 1"
   response_list=[]
   response = session.execute(stmt)
   for val in response:
      response_list.append(val)
   jsonresponse_1 = [{"complaint_type": x.complaint_type, "incident_zip": x.incident_zip, "total":x.total} for x in response_list]

# Picasso ('Graffiti')
   title = "The 411 on the 311"
   stmt = "SELECT * FROM awards WHERE complaint_type = 'Graffiti' limit 1"
   response_list=[]
   response = session.execute(stmt)
   for val in response:
      response_list.append(val)
   jsonresponse_2 = [{"complaint_type": x.complaint_type, "incident_zip": x.incident_zip, "total":x.total} for x in response_list]

#Taxi ('Taxi Complaint')
   title = "The 411 on the 311"
   stmt = "SELECT * FROM awards WHERE complaint_type = 'Taxi Complaint' limit 1"
   response_list=[]
   response = session.execute(stmt)
   for val in response:
      response_list.append(val)
   jsonresponse_3 = [{"complaint_type": x.complaint_type, "incident_zip": x.incident_zip, "total":x.total} for x in response_list]

#Trees ('Overgrown Trees/Bushes')
   title = "The 411 on the 311"
   stmt = "SELECT * FROM awards WHERE complaint_type = 'Overgrown Tree/Branches' limit 1"
   response_list=[]
   response = session.execute(stmt)
   for val in response:
      response_list.append(val)
   jsonresponse_4 = [{"complaint_type": x.complaint_type, "incident_zip": x.incident_zip, "total":x.total} for x in response_list]

#Very Vocal ('Noise')
   title = "The 411 on the 311"
   stmt = "SELECT * FROM awards WHERE complaint_type = 'Noise' limit 1"
   response_list=[]
   response = session.execute(stmt)
   for val in response:
      response_list.append(val)
   jsonresponse_5 = [{"complaint_type": x.complaint_type, "incident_zip": x.incident_zip, "total":x.total} for x in response_list]

# Rodent ('Rodent')
   title = "The 411 on the 311"
   stmt = "SELECT * FROM awards WHERE complaint_type = 'Rodent' limit 1"
   response_list=[]
   response = session.execute(stmt)
   for val in response:
      response_list.append(val)
   jsonresponse_6 = [{"complaint_type": x.complaint_type, "incident_zip": x.incident_zip, "total":x.total} for x in response_list]
   return render_template("awards.html", data=jsonresponse_1, data2=jsonresponse_2, data3=jsonresponse_3, data4=jsonresponse_4, data5=jsonresponse_5, data6=jsonresponse_6)

#@aap.route('/typesofcalls')
@app.route('/typesofcalls', methods=['GET','POST'])
def zipcodeComplaints():
    if request.method=="GET":
        return render_template('types_of_calls.html')
    if request.method=="POST":
        response_list=[]

        if 'incident_zip' in request.form: 
           incident_zip = request.form['incident_zip']

    stmt = "SELECT * FROM types_of_calls WHERE incident_zip=%s"
    response = session.execute(stmt, parameters=[int(incident_zip)])
    for val in response:
       response_list.append(val)
    jsonresponse = [{"complaint_type": x.complaint_type, "incident_zip": x.incident_zip, "total":x.total} for x in response_list]
    return render_template('types_of_calls.html', results = jsonresponse)
    #return jsonify(data=jsonresponse)

@app.route("/techspecifications")
def techspecifications():
   title = "The 411 on the 311"
   return render_template("aboutme.html", title = title)
