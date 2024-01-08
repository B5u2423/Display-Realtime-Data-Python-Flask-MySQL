document.addEventListener('DOMContentLoaded', function () {
    // var socket = io.connect('http://' + document.domain + ':' + location);
    var socket = io.connect();
    
    var ctx1 = document.getElementById('sensorChart').getContext('2d');
    // SETUP Blocks
    const chart_data = {
        labels: [],
        datasets: [
            {
                label: 'Temperature',
                borderColor: 'rgb(75, 192, 192)',
                borderWidth: 3,
                data: [],
            },{
                label: 'Humidity',
                borderColor: 'rgb(255, 99, 132)',
                borderWidth: 3,
                data: [],
            }
        ],
    };
    
    // CONFIG Blocks
    const chart_config = {
        type: 'line',
        data: chart_data,
    };
    
    // create the chart
    var sensorChart = new Chart(ctx1, chart_config);
    const MAX_ITEM_COUNT = 15;

    // SocketIO event handler for real-time updates
    socket.on('update_data', function (data) {
        console.log("Received sensorData :: " + data.labels + " :: " + data.humidity + " :: " +  data.temperature); // for debugging

        if (sensorChart.data.labels.length > MAX_ITEM_COUNT) {
            removeFirstItem();
        }
        addItemToLast(data.labels, data.temperature, data.humidity);
    });

    function addItemToLast(label, temperature, humidity) {
        // add new data
        sensorChart.data.labels.push(label);        
        sensorChart.data.datasets[0].data.push(temperature);
        sensorChart.data.datasets[1].data.push(humidity); 
        // update the chart
        sensorChart.update();
    }
    
    function removeFirstItem() {
        sensorChart.data.labels.splice(0, 1);
        sensorChart.data.datasets.forEach((dataset) => {
            dataset.data.shift();
    });
    }
});
