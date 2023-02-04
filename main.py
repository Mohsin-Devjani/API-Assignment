from flask import Flask, jsonify, request

app = Flask(__name__)

todo_list_data = [{"id":1, "name":"write todo list app"}]

@app.route(rule='/', methods=['GET'])
def main():
    return "hello world"

@app.route(rule='/todo/api/v1/create_todo', methods=['POST'])
def create_todo():
    if request.method == "POST":
        data = request.get_json()
        return jsonify(data)
    
@app.route(rule='/pagination/<int:number>/', methods=['GET'])
def pagination(number):
    return f"on page: {number}"

@app.route(rule='/user/<string:user_name>/', methods=['GET'])
def get_user(user_name):
    try:
        return f"User Name: {user_name}", 200
    except:
        return "server failure", 500

@app.route(rule='/post_data', methods=['GET', 'POST'])
def post_data():
    if request.method == "GET":
        return "invalid request/Get request"
    if request.method == "POST":
        # picking json data send from post request
        data = request.get_json()
        return jsonify({"user_data": data})

if __name__=='__main__':
    app.run(host="0.0.0.0", port="8080", debug=True)


