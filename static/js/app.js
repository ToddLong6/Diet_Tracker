document.addEventListener("DOMContentLoaded", () => {
  new Chart(document.querySelector('#lineChart'),{
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: 'Weight',
        data: [65, 59, 80, 81, 56, 55, 40],
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
});