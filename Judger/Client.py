import json
from server.Server import JudgeServer
from flask import Flask, request, Response
from server.Validate import Validate
import gevent.monkey

gevent.monkey.patch_all()

app = Flask(__name__)

@app.route('/judge',methods=['POST'])
def get_judge_result():
	data = json.loads(request.get_data().decode('utf-8'))
	validate = Validate(data)

	#判断输入参数是否合法
	if(not validate.validateAgrs()):
		result = {
			'errorMessage':'agrs are not legal',
			'status':'fail'
		}
		return Response(json.dumps(result), mimetype='application/json')
	#判断标准输入是否为空null或者为空字符串
	for item in data['test_cases']:
		index = data['test_cases'].index(item)
		if item['stdin'] == None or len(item['stdin']) == 0:
			data['test_cases'][index]['stdin'] = ' '

	sever = JudgeServer(data)
	result = sever.judge()
	return Response(json.dumps(result), mimetype='application/json')
	
@app.route('/status', methods=['GET'])
def get_status():
	status ={
 		    'memory_percent':str(psutil.virtual_memory().percent)+'%',
            'available_memeory':round(psutil.virtual_memory().available/1024**3,2)
 		}
	return Response(json.dumps(status), mimetype='application/json')

#gunicorn -k gevent -c gunicorn.conf Client:app
if __name__ == '__main__':
	app.run(debug=True)
