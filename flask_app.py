from flask import Flask, render_template
#import twitter_test
# Flask クラスのインスタンスを作って-> appに代入
app = Flask(__name__)

@app.route("/")
def index():
    # word = "aaa"
    # test_word = twitter_test.main(word)
    # python(test_word)
    return render_template('index.html', message= "test_word")

@app.route("/page1")
def page1():
    return render_template('page1.html', message="こんにちは")

@app.route("/chart")
def chart():
    return render_template('chart.html')

if __name__ == "__main__":
    # flaskの起動
    app.run(debug=True, host="0.0.0.0")
