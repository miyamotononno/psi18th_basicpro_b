import React, { Component } from "react";
import { css } from "glamor";

let form = css({
  textAlign: "center",
  fontFamily: "Helvetica Neue",
  padding: "10px",
  border: "none",
  background: "rgba(0, 0, 0, 0.003)",
  boxShadow: "inset 0 -2px 1px rgba(0,0,0,0.03)"
});

let input_css = css({
  padding: "10px 20px",
  margin: "10px",
  fontSize: "1.3em",
  fontFamily: "Helvetica Neue",
  color: "#aaa",
  border: "solid 1px #ccc",
  //margin: "0 0 20px",
  borderRadius: "3px",
  boxShadow: "inner 0 0 4px rgba(0, 0, 0, 0.2)",
  fontWeight: "300",
  ":focus": {
    outline: "0",
    border: "solid 1px"
  }
});

export default class Form extends Component {
  render() {
    const { mainText,handleChange } = this.props;
    return (
      <div {...form}>
        <form id="formTag" name="todoform" >
          <input
            {...input_css}
            name="mainTextName"
            type="text"
            value={mainText}
            placeholder="検索ワードを入力"
            size="30"
            maxLength="30"
            onChange={handleChange}
          />
          <br />
        </form>
      </div>
    );
  }
}
