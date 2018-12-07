from bottle import route, run

@route('/sysdig')
def sysdig():
return "<h1>Sysdig Rocks CI/CD!</h1>"

run(host='0.0.0.0', port=8001, debug=True)
