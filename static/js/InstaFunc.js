var positiveValue = 1;
var neutralValue = 1;
var negativeValue = 1;
var bar_label1 = "1位";
var bar_label2 = "2位";
var bar_label3 = "3位";
var bar_label4 = "4位";
var bar_label5 = "5位";
var bar_count1 = 0;
var bar_count2 = 0;
var bar_count3 = 0;
var bar_count4 = 0;
var bar_count5 = 0;


var input_value = "instagram";
function onButtonSubmit(){

  input_value = document.form1.inputboxname.value;
  $.ajax({
    type: 'post',
    url: "/twitter",
    data: JSON.stringify({ 'value': input_value }),
    contentType: 'application/JSON',
    dataType: 'JSON',
    scriptCharset: 'utf-8',
    success: function (data) {
      positiveValue = data['result'][0][0];
      negativeValue = data['result'][0][1];
      neutralValue = data['result'][0][2];
      bar_label1 = data['result'][1][0][0];
      bar_label2 = data['result'][1][1][0];
      bar_label3 = data['result'][1][2][0];
      bar_label4 = data['result'][1][3][0];
      bar_label5 = data['result'][1][4][0];
      bar_count1 = data['result'][1][0][1];
      bar_count2 = data['result'][1][1][1];
      bar_count3 = data['result'][1][2][1];
      bar_count4 = data['result'][1][3][1];
      bar_count5 = data['result'][1][4][1];
      piechart.data.datasets[0].data[0] = positiveValue;
      piechart.data.datasets[0].data[1] = negativeValue;
      piechart.data.datasets[0].data[2] = neutralValue;
      barchart.data.labels[0] = bar_label1
      barchart.data.labels[1] = bar_label2
      barchart.data.labels[2] = bar_label3
      barchart.data.labels[3] = bar_label4
      barchart.data.labels[4] = bar_label5
      barchart.data.datasets[0].data[0] = bar_count1;
      barchart.data.datasets[0].data[1] = bar_count2;
      barchart.data.datasets[0].data[2] = bar_count3;
      barchart.data.datasets[0].data[3] = bar_count4;
      barchart.data.datasets[0].data[4] = bar_count5;
      piechart.update();
      barchart.update();
    },
    error: function (data) {
      console.error("error post clip");
    }
  });
  return false;
}

var piechart = new Chart(document.getElementById("instaPiechart"), {
  type: "doughnut",
  data: {
    labels: ["ポジティブ","中立","ネガティブ"],
    datasets: [
      {
        data: [Math.random(), Math.random(), Math.random()],
        backgroundColor: [
          "rgb(255, 99, 132)",
          "rgb(154,130,183)",
          "rgb(54, 162, 235)"
        ]
      }
    ]
  }
})

var barchart = new Chart(document.getElementById("instaBargraph"),{
    type: "bar",
    data:{
      labels: [bar_label1, bar_label2, bar_label3, bar_label4, bar_label5],
      datasets: [{
        data: [Math.random(),Math.random(),Math.random(), Math.random(), Math.random()],
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
       xAxes: [{
         display: true,
         barPercentage: 0.4,
         categoryPercentage: 0.4,
         scaleLabel: {
            display: true,
            labelString: '関連ワード',
            fontSize: 18
         },
         ticks: {
             fontSize: 18
         },
       }],
     },
     layout: {
       padding: {
           left: 100,
           right: 50,
           top: 0,
           bottom: 0
       }
     }
    }
});
