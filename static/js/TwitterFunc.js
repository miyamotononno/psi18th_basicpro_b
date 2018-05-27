var tweet_positiveValue = 1;
var tweet_neutralValue = 1;
var tweet_negativeValue = 1;
var tweet_bar_label1 = "1位";
var tweet_bar_label2 = "2位";
var tweet_bar_label3 = "3位";
var tweet_bar_label4 = "4位";
var tweet_bar_label5 = "5位";
var tweet_bar_count1 = 1;
var tweet_bar_count2 = 0.8;
var tweet_bar_count3 = 0.6;
var tweet_bar_count4 = 0.4;
var tweet_bar_count5 = 0.2;


var tweet_input_value = "twitter";
function onButtonTwitter(){

  tweet_input_value = document.form1.inputboxname.value;
  $.ajax({
    type: 'post',
    url: "/twitter",
    data: JSON.stringify({ 'value': tweet_input_value }),
    contentType: 'application/JSON',
    dataType: 'JSON',
    scriptCharset: 'utf-8',
    success: function (data) {
      tweet_positiveValue = data['result'][0][0];
      tweet_negativeValue = data['result'][0][1];
      tweet_neutralValue = data['result'][0][2];
      tweet_bar_label1 = data['result'][1][0][0];
      tweet_bar_label2 = data['result'][1][1][0];
      tweet_bar_label3 = data['result'][1][2][0];
      tweet_bar_label4 = data['result'][1][3][0];
      tweet_bar_label5 = data['result'][1][4][0];
      tweet_bar_count1 = data['result'][1][0][1];
      tweet_bar_count2 = data['result'][1][1][1];
      tweet_bar_count3 = data['result'][1][2][1];
      tweet_bar_count4 = data['result'][1][3][1];
      tweet_bar_count5 = data['result'][1][4][1];
      tweet_piechart.data.datasets[0].data[0] = tweet_positiveValue;
      tweet_piechart.data.datasets[0].data[1] = tweet_negativeValue;
      tweet_piechart.data.datasets[0].data[2] = tweet_neutralValue;
      tweet_barchart.data.labels[0] = tweet_bar_label1
      tweet_barchart.data.labels[1] = tweet_bar_label2
      tweet_barchart.data.labels[2] = tweet_bar_label3
      tweet_barchart.data.labels[3] = tweet_bar_label4
      tweet_barchart.data.labels[4] = tweet_bar_label5
      tweet_barchart.data.datasets[0].data[0] = tweet_bar_count1;
      tweet_barchart.data.datasets[0].data[1] = tweet_bar_count2;
      tweet_barchart.data.datasets[0].data[2] = tweet_bar_count3;
      tweet_barchart.data.datasets[0].data[3] = tweet_bar_count4;
      tweet_barchart.data.datasets[0].data[4] = tweet_bar_count5;
      tweet_piechart.update();
      tweet_barchart.update();
    },
    error: function (data) {
      console.error("error post clip");
    }
  });
  return false;
}

var tweet_piechart = new Chart(document.getElementById("twitterPiechart"), {
  type: "doughnut",
  data: {
    labels: ["ポジティブ","ネガティブ","中立"],
    datasets: [
      {
        data: [tweet_positiveValue, tweet_negativeValue, tweet_neutralValue],
        backgroundColor: [
          "rgb(255, 99, 132)",
          "rgb(154,130,183)",
          "rgb(54, 162, 235)"
        ]
      }
    ]
  }
})

var tweet_barchart = new Chart(document.getElementById("twitterBargraph"),{
    type: "bar",
    data:{
      labels: [tweet_bar_label1, tweet_bar_label2, tweet_bar_label3, tweet_bar_label4, tweet_bar_label5],
      datasets: [{
        data: [tweet_bar_count1,tweet_bar_count2,tweet_bar_count3, tweet_bar_count4, tweet_bar_count5],
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
