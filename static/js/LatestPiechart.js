var tweet_positiveValue = 1;
var tweet_negativeValue = 1.2;
var tweet_neutralValue = 0.8;
var insta_positiveValue = 1;
var insta_negativeValue = 1.2;
var insta_neutralValue = 0.8;


new Chart(document.getElementById("LatestTwitterPiechart"), {
  type: "doughnut",
  data: {
    labels: ["ポジティブ","ネガティブ","中立"],
    datasets: [
      {
        data: [tweet_positiveValue, tweet_negativeValue, tweet_neutralValue],
        backgroundColor: [
          "rgb(255, 99, 132)",
          "rgb(154,130,183)",
          "rgb(0,255,0)"
        ]
      }
    ]
  }
})

new Chart(document.getElementById("LatestInstaPiechart"), {
  type: "doughnut",
  data: {
    labels: ["ポジティブ","ネガティブ","中立"],
    datasets: [
      {
        data: [insta_positiveValue, insta_negativeValue, insta_neutralValue],
        backgroundColor: [
          "rgb(255, 99, 132)",
          "rgb(154,130,183)",
          "rgb(0,255,0)"
        ]
      }
    ]
  }
})
