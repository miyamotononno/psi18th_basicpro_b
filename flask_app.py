import json
from flask import Flask, render_template, request, jsonify
import twitter_test
# Flask クラスのインスタンスを作って-> appに代入
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/chart")
def chart():
    return render_template('chart.html')

@app.route('/twitter', methods=['POST'])
def twitter():
    data = json.loads(request.data)
    #print("data:", data)
    result = twitter_test.main(data["value"])
    # print("result:", result)
    # print("result[1]",result[1])
    # print("result[1][0]",result[1][0])
    # print("result[1][0][0]",result[1][0][0])
    return jsonify({'result': result})

if __name__ == "__main__":
    # flaskの起動
    app.run(debug=True, host="0.0.0.0")

#感情分析をmain()関数のp_n_neuでreturnされているものを用いる
#関連ワードはmain()関数のsorted_list[:10]
