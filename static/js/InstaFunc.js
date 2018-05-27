var insta_positiveValue = 1;
var insta_neutralValue = 1;
var insta_negativeValue = 1;
var insta_bar_label1 = "1位";
var insta_bar_label2 = "2位";
var insta_bar_label3 = "3位";
var insta_bar_label4 = "4位";
var insta_bar_label5 = "5位";
var insta_bar_count1 = 0;
var insta_bar_count2 = 0;
var insta_bar_count3 = 0;
var insta_bar_count4 = 0;
var insta_bar_count5 = 0;


var insta_input_value = "instagram";
function onButtonInstagram(){

  insta_input_value = document.form1.inputboxname.value;
  $.ajax({
    type: 'post',
    url: "/instagram",
    data: JSON.stringify({ 'value': insta_input_value }),
    contentType: 'application/JSON',
    dataType: 'JSON',
    scriptCharset: 'utf-8',
    success: function (data) {
      insta_positiveValue = data['result'][0][0];
      insta_negativeValue = data['result'][0][1];
      insta_neutralValue = data['result'][0][2];
      insta_bar_label1 = data['result'][1][0][0];
      insta_bar_label2 = data['result'][1][1][0];
      insta_bar_label3 = data['result'][1][2][0];
      insta_bar_label4 = data['result'][1][3][0];
      insta_bar_label5 = data['result'][1][4][0];
      insta_bar_count1 = data['result'][1][0][1];
      insta_bar_count2 = data['result'][1][1][1];
      insta_bar_count3 = data['result'][1][2][1];
      insta_bar_count4 = data['result'][1][3][1];
      insta_bar_count5 = data['result'][1][4][1];
      insta_piechart.data.datasets[0].data[0] = insta_positiveValue;
      insta_piechart.data.datasets[0].data[1] = insta_negativeValue;
      insta_piechart.data.datasets[0].data[2] = insta_neutralValue;
      insta_barchart.data.labels[0] = insta_bar_label1;
      insta_barchart.data.labels[1] = insta_bar_label2;
      insta_barchart.data.labels[2] = insta_bar_label3;
      insta_barchart.data.labels[3] = insta_bar_label4;
      insta_barchart.data.labels[4] = insta_bar_label5;
      insta_barchart.data.datasets[0].data[0] = insta_bar_count1;
      insta_barchart.data.datasets[0].data[1] = insta_bar_count2;
      insta_barchart.data.datasets[0].data[2] = insta_bar_count3;
      insta_barchart.data.datasets[0].data[3] = insta_bar_count4;
      insta_barchart.data.datasets[0].data[4] = insta_bar_count5;
      insta_piechart.update();
      insta_barchart.update();
    },
    error: function (data) {
      console.error("error post clip");
    }
  });
  return false;
}

var insta_piechart = new Chart(document.getElementById("instaPiechart"), {
  type: "doughnut",
  data: {
    labels: ["ポジティブ","ネガティブ","中立"],
    datasets: [
      {
        data: [insta_positiveValue,insta_negativeValue,insta_neutralValue],
        backgroundColor: [
          "rgb(255, 99, 132)",
          "rgb(154,130,183)",
          "rgb(54, 162, 235)"
        ]
      }
    ]
  }
})

var insta_barchart = new Chart(document.getElementById("instaBargraph"),{
    type: "bar",
    data:{
      labels: [insta_bar_label1, insta_bar_label2, insta_bar_label3, insta_bar_label4, insta_bar_label5],
      datasets: [{
        data: [insta_bar_count1,insta_bar_count2,insta_bar_count3,insta_bar_count4 ,insta_bar_count5],
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
