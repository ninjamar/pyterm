import flask
import ast
import subprocess
import sys
app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/run',methods=['POST'])
def run():
    try:
        if flask.request.method == 'POST':
            data = ast.literal_eval(flask.request.data.decode())
            cmd = data['cmd'].split()
            print(cmd)
            if 'stdin' in data:
                p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
                out,err = p.communicate(data['stdin'])
            else:
                p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                out,err = p.communicate()
                resp = flask.make_response(out.decode()+err.decode())
                resp.headers['Content-Type'] = 'text'
                return resp
        else:
            return 'must make POST requests'
    except Exception as e:
        return str(e)

@app.route('/help')
def help():
    return flask.redirect('https://scratch.mit.edu/discuss/topic/510569')
app.run(host=sys.argv[1],port=sys.argv[2])
