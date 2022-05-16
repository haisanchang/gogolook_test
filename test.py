from flask import Flask, jsonify, request
import configparser

#取得配置檔參數
config = configparser.ConfigParser()
config.read(['config.ini'])
port = int(config['GOGOLOOK']['port'])

app = Flask(__name__)

temp_data = []
count = 0

#取得所有資料
@app.route('/tasks', methods=['GET'])
def tasks():
	resp = {"result": temp_data}
	
	return jsonify(resp)

#創建單筆資料
@app.route('/task', methods=['POST'])
def task():
	
	global count

	try:
		req_data = request.get_json()
		name = req_data['name'] 
	except:
		resp = {"Status": "failed", "Message":"Lack of necessary parameters"}
		return jsonify(resp), 400
	
	count += 1
	data = {"name": str(name), "status": 0, "id": count}
	temp_data.append(data)
	
	resp = {"result": data}
	
	return jsonify(resp), 201


#更新資料
@app.route('/task/<int:id>', methods=['PUT'])
def update_task(id):
	try:
		req_data = request.get_json()
		id_int = int(req_data['id'])

	except:
		resp = {"Status": "failed", "Message":"Lack of necessary parameters"}
		return jsonify(resp), 400
	
	for d in temp_data:
		if id_int == d['id']:
			d['name'] = req_data['name']
			d['status'] = req_data['status']
			
			resp = {"result": d}

	return	jsonify(resp), 200


#刪除資料
@app.route('/task/<int:id>', methods=['DELETE'])
def delete_task(id):
	for indx, d in enumerate(temp_data):
		
		if d['id'] == id:
			del temp_data[indx]	
			return jsonify(None), 200

	resp = {"Status": "failed", "Message":"The ID not found."}
	return jsonify(resp), 400
			
if __name__ == '__main__': 
	app.run(debug=True, port= port, threaded=True, host = '0.0.0.0')