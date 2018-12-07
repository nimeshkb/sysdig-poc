from bottle import route, run

@route('/sysdig')
def sysdig():
return "<body style="background-color:powderblue;"><h1>Sysdig Rocks CI/CD!</h1><p>What do you think?</p>"

run(host='0.0.0.0', port=8001, debug=True)
