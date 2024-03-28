console.log("running index.js on frontend");

// big chart - historical (day) energy production and consumption
// two lines

const ctx5 = document.getElementById("canvas5");

function generateArraySkippingFive() {
  let array = [];
  for (let i = 1; i <= 700; i++) {
    array.push(i);
  }
  return array;
}

const labels = generateArraySkippingFive();

// fetch data
fetch("/get-data/aaron@gmail.com")
  .then((response) => {
    if (!response.ok) {
      throw new Error("Network response was not ok " + response.statusText);
    }
    return response.json();
  })
  .then((data) => {
    console.log(data);
    // res was ok
    // create chart
    // Arrays to hold the extracted values
    let key1Array = [];
    let key2Array = [];

    // Using forEach to iterate over the array
    data.forEach((item) => {
      key1Array.push(item["consumption"]);
      key2Array.push(item["production"]);
    });

    console.log(key1Array);
    console.log(key2Array);

    const lastItem = [
      key1Array[key1Array.length - 1],
      key2Array[key2Array.length - 1],
    ];
    console.log(lastItem);
    document.getElementById("pred-output").innerText = lastItem[1] + " kW/h";
    document.getElementById("pred-cons").innerText = lastItem[0] + " kW/h";
    document.getElementById("current-prod").innerText = lastItem[1] + " kW/h";
    new Chart(ctx5, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Consumed",
            data: key1Array,
            borderWidth: 1,
            fill: true,
            backgroundColor: "#2f93a270",
            tension: 0.3,
          },
          {
            label: "Produced",
            data: key2Array,
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
    // document.getElementById("someElement").textContent = data.name;
  })
  .catch((error) => {
    console.error("There has been a problem with your fetch operation:", error);
  });

// fetch for prediction
fetch("/get-prediction/aaron@gmail.com")
  .then((response) => {
    if (!response.ok) {
      throw new Error("Network response was not ok " + response.statusText);
    }
    return response.json();
  })
  .then((data) => {
    console.log("getting prediction...");
    console.log(data);
    // res was ok

    // document.getElementById("someElement").textContent = data.name;
  })
  .catch((error) => {
    console.error("There has been a problem with your fetch operation:", error);
  });
