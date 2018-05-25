from flask import Flask, render_template
#import twitter_test
# Flask クラスのインスタンスを作って-> appに代入
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', message= "test_word")

@app.route("/chart")
def chart():
    return render_template('chart.html')

if __name__ == "__main__":
    # flaskの起動
    app.run(debug=True, host="0.0.0.0")
