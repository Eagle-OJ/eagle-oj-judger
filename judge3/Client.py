import json
from server.Server import JudgeServer
from flask import Flask, request, Response
import gevent.monkey

gevent.monkey.patch_all()

app = Flask(__name__)
@app.route('/json',methods=['POST'])
def get_judge_result():
	data = json.loads(request.get_data().decode('utf-8'))
	#判断标准输入是否为空null或者为空字符串
	for item in data['test_cases']:
		index = data['test_cases'].index(item)
		if item['stdin'] == None or len(item['stdin']) == 0:
			data['test_cases'][index]['stdin'] = ' '

	sever = JudgeServer(data)
	result = sever.judge()
	return Response(json.dumps(result), mimetype='application/json')

#gunicorn -k gevent -c gunicorn.conf Client:app
if __name__ == '__main__':
	app.run(debug=True)