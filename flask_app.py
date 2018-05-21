from flask import Flask, render_template

# Flask クラスのインスタンスを作って-> appに代入
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', message="こんにちは")

@app.route("/page1")
def page1():
    return render_template('page1.html', message="こんにちは")

if __name__ == "__main__":
    # flaskの起動
    app.run(debug=True, host="0.0.0.0")
