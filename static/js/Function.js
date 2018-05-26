
var positiveValue = 1;
var neutralValue = 1;
var negativeValue = Math.random();

var input_value = 1;
function onButtonSubmit(){

  input_value = parseFloat(document.form1.inputboxname.value);
      $.ajax({
      type: 'post',
      url: "/twitter",
      data: JSON.stringify({ 'value': input_value }),
      contentType: 'application/JSON',
      dataType: 'JSON',
      scriptCharset: 'utf-8',
      success: function (data) {
        // Success
        // data['result']の値を使って表示する
        alert(json_post(input_value));
        console.log(data['result'])
      },
      error: function (data) {
        // Error
        console.error("error post clip");
      }
    });

  piechart.data.datasets[0].data[0] = input_value;
  barchart.data.datasets[0].data[0] = positiveValue;
  piechart.update();
  barchart.update();

  return false;
}

var piechart = new Chart(document.getElementById("myPiechart"), {
  type: "doughnut",
  data: {
    labels: ["ポジティブ","中立","ネガティブ"],
    datasets: [
      {
        data: [input_value, neutralValue, negativeValue], //本当はMath.random()
        backgroundColor: [
          "rgb(255, 99, 132)",
          "rgb(154,130,183)",
          "rgb(54, 162, 235)"
        ]
      }
    ]
  }
})

var barchart = new Chart(document.getElementById("myBargraph"),{
    type: "bar",
    data:{
      labels: ['1位','2位','3位'],
      datasets: [{
        data: [input_value ,Math.random(),Math.random()],
        backgroundColor: ['#FF4444', '#4444FF', '#44BB44', '#FFFF44', '#FF44FF']
      }]
    },
    options:{
      responsive: true,
      lengends:{
        display: false
      },
      title:{
        display: true,
        fontSize: 18,
        text: '関連ワード'
      },
      scales: {
        yAxis:[{
          display: true,
          scaleLabel:{
            display: true,
            labelString: '縦軸ラベル',
            fontSize: 18
          },
          ticks:{
            min: 0,
            max: 30,
            fontSize: 18,
            stepSize: 5
          },
       }],
       xAxes: [{                         //x軸設定
         display: true,                //表示設定
         barPercentage: 0.4,           //棒グラフ幅
         categoryPercentage: 0.4,      //棒グラフ幅
         scaleLabel: {                 //軸ラベル設定
            display: true,             //表示設定
            labelString: '横軸ラベル',  //ラベル
            fontSize: 18               //フォントサイズ
         },
         ticks: {
             fontSize: 18             //フォントサイズ
         },
       }],
     },
     layout: {
       padding: {                          //余白設定
           left: 100,
           right: 50,
           top: 0,
           bottom: 0
       }
     }
    }
});
