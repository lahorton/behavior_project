let ctx = document.getElementById('myChart').getContext('2d');
let myChart = new Chart(ctx, {
  type: 'line',
  data: {
    // I want lebels to be dates, depending on progress reports
    labels: ['M', 'T', 'W', 'T', 'F', 'S', 'S'],
    // I want dataset to be labels = behaviors and data = ratings
    datasets: [{
      label: 'apples',
      data: [12, 19, 3, 17, 6, 3, 7],
      backgroundColor: "rgba(153,255,51,0.4)"
    }, {
      label: 'oranges',
      data: [2, 29, 5, 5, 2, 3, 10],
      backgroundColor: "rgba(255,153,0,0.4)"
    }]
  }
});