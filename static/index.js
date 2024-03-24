console.log("running index.js on frontend");

// big chart - historical (day) energy production and consumption
// two lines

const ctx5 = document.getElementById("canvas5");

new Chart(ctx5, {
  type: "line",
  data: {
    labels: ["01", "02", "03", "04", "05", "06"],
    datasets: [
      {
        label: "Consumed",
        data: [1, 19, 3, 5, 2, 3],
        borderWidth: 1,
        fill: true,
        backgroundColor: "#2f93a270",
        tension: 0.3,
      },
      {
        label: "Produced",
        data: [10, 5, 11, 6, 9, 2],
        borderWidth: 1,
        fill: true,
        backgroundColor: "#04318b6e",
        tension: 0.5,
      },
    ],
  },
  options: {
    maintainAspectRatio: false,

    scales: {
      y: {
        display: false,
        beginAtZero: true,
        grid: {
          display: false,
        },
      },
    },
  },
});

// fetch data
fetch("/get-data")
  .then((response) => {
    if (!response.ok) {
      throw new Error("Network response was not ok " + response.statusText);
    }
    return response.json();
  })
  .then((data) => {
    console.log(data);
    document.getElementById("someElement").textContent = data.name;
  })
  .catch((error) => {
    console.error("There has been a problem with your fetch operation:", error);
  });
