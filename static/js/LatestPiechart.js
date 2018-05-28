// var tweet_positiveValue = 238;
// var tweet_negativeValue = 272;
// var tweet_neutralValue = 411;
// var insta_positiveValue = 1763;
// var insta_negativeValue = 2206;
// var insta_neutralValue = 5600;

var tweet_positiveValue = 1763;
var tweet_negativeValue = 2206;
var tweet_neutralValue = 5600;
var insta_positiveValue = 238;
var insta_negativeValue = 272;
var insta_neutralValue = 411;

new Chart(document.getElementById("LatestTwitterPiechart"), {
  type: "doughnut",
  data: {
    labels: ["ポジティブ","中立","ネガティブ"],
    datasets: [
      {
        data: [tweet_positiveValue, tweet_negativeValue, tweet_neutralValue],
        backgroundColor: [
          "rgb(255, 99, 132)",
          "rgb(0,255,0)",
          "rgb(154,130,183)"
        ]
      }
    ]
  }
})

new Chart(document.getElementById("LatestInstaPiechart"), {
  type: "doughnut",
  data: {
    labels: ["ポジティブ","中立","ネガティブ"],
    datasets: [
      {
        data: [insta_positiveValue, insta_negativeValue, insta_neutralValue],
        backgroundColor: [
          "rgb(255, 99, 132)",
          "rgb(0,255,0)",
          "rgb(154,130,183)"
        ]
      }
    ]
  }
})
