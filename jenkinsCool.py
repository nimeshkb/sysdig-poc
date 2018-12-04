from bottle import route, run

@route('/sysdig')
def sysdig():
    return "Sysdig Rocks!"

run(host='0.0.0.0', port=8001, debug=True)
