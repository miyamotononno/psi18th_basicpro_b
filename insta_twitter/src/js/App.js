import React, { Component } from 'react';
import Form from "./form";
import { css } from "glamor";

let headerText = css({
  color: "rgba(80, 200, 120)",
  fontFamily: "Helvetica Neue"
});

let twoColumnBox = css({
  height: "100vh",
  width: "100%",
  textAlign: "center",
  display: "flex",
  alignItems: "center",
  justifyContent: "center"
});

let eachText = css({
  marginBottom: "10%",
  textAlign: "center",
  fontFamily: "Helvetica Neue",
  padding: "500px 300px 300px 300px",
  border: "none",
  background: "rgba(0, 0, 0, 0.003)",
  boxShadow: "inset 0 -2px 1px rgba(0,0,0,0.03)"
});

class App extends Component {

  state ={
    mainText: ""
  }

  handleChange = e => {
    this.setState({
      mainText: e.target.value
    });
  };

  render() {

    return (
      <div className="App">
        <header className="App-header">
          <h1 {...headerText}>InstagramとTwitterの違い</h1>
          <Form
            mainText={this.state.mainText}
            handleChange={this.handleChange.bind(this)}
          />
        </header>
        <body>
          <div {...twoColumnBox}>
            <div {...eachText}>
              <h2>Twitter</h2>
              <p>関連ワード</p>
            </div>
            <div {...eachText}>
              <h2>Instagram</h2>
              <p>関連ワード</p>
            </div>
          </div>
        </body>
      </div>
    );
  }
}

export default App;
