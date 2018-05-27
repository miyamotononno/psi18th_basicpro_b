import json
from flask import Flask, render_template, request, jsonify
import function_teamc as ft
# Flask クラスのインスタンスを作って-> appに代入
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/twitter', methods=['POST'])
def twitter():
    data = json.loads(request.data)
    print("data:", data)
    result = ft.main(data["value"])
    return jsonify({'result': result})

@app.route('/instagram', methods=['POST'])
def instagram():
    data = json.loads(request.data)
    print("instaのdata:", data)
    result = ft.insta(data["value"])
    return jsonify({'result': result})

if __name__ == "__main__":
    # flaskの起動
    app.run(debug=True, host="0.0.0.0")

#感情分析をmain()関数のp_n_neuでreturnされているものを用いる
#関連ワードはmain()関数のsorted_list[:10]
