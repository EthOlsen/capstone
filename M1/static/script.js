// script.js

document.addEventListener('DOMContentLoaded', function () {
    const socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', function () {
        console.log('Connected to Socket.IO');
        socket.emit('get_arp_results');
    });

    socket.on('disconnect', function () {
        console.log('Disconnected from Socket.IO');
    });

    var layout = {
        title: 'Protocol Distribution',
    };

    const maxDataPoints = 200;

    // Initialize the x and y arrays with empty values
    //var xValues = Array(maxDataPoints).fill('');
    //var yValues = Array(maxDataPoints).fill(0);
    var xValues = [];
    var yValues = [];

    var chartData = [{
        type: 'pie',
        x: [],
        y: [],
    }];

    Plotly.newPlot('protodist', chartData, layout);

    // Initialize Throughput Over Time Line Graph
    var throughputLayout = {
        title: 'Throughput Over Time',
        xaxis: { title: 'Time' },
        yaxis: { title: 'Throughput' },

    };

    var throughputChartData = [{
        type: 'line',
        mode: 'lines+markers',
        x: xValues,
        y: yValues,

    }];

    Plotly.newPlot('throughputGraph', throughputChartData, throughputLayout);

    var topTalkersLayout = {
        title: 'Top Talkers',
    };

    var topTalkersChartData = [{
        type: 'bar',
        x: [],
        y: [],
    }];

    Plotly.newPlot('topTalkers', topTalkersChartData, topTalkersLayout);

    // 

    socket.on('update_data', function (data) {
        //console.log('updated_data');

        var protocols = Object.keys(data);
        var counts = Object.values(data);

        Plotly.update('protodist', { labels: [protocols], values: [counts] });
    });

    // 

    socket.on('dnspacket', function (data) {
        //console.log('dnspacket');
        var dats = data.split(':');

        var dnsList = document.getElementById('dnsTableBody');
        var listItem = document.createElement('tr');
        listItem.classList.add('bg-blue');
        listItem.innerHTML = `<td>${dats[1]}</td><td>192.168.1.1</td><td>${dats[0]}</td>`;
        dnsList.appendChild(listItem);
    });

    socket.on('arp_results', function (data) {
        var arpTable = document.getElementById('arpTableBody');
        arpTable.innerHTML = '';

        data.clients.forEach(client => {
            var listItem = document.createElement('tr');
            listItem.classList.add('bg-blue');
            listItem.innerHTML = `<td>${client.ip}</td><td>${client.mac}</td>`;
            arpTable.appendChild(listItem);
        });
    });

    var top_talkers = {};
    socket.on('update_top_talkers', function (data) {
        //console.log('Cupdate_top_talkers');

        // Update top_talkers variable
        top_talkers = data.topTalkers;
        ports = data.ports
        const portsList = document.getElementById('portsResults');
        portsList.innerHTML = '';

        ports.forEach(client => {
            const listItem = document.createElement('li');
            listItem.textContent = client;
            portsList.appendChild(listItem);
        });

        // Sort the top_talkers object by packet count in descending order
        var sortedTopTalkers = Object.entries(top_talkers).sort((a, b) => b[1] - a[1]);
        // Select the top ten IP addresses and their packet counts
        var topTenTalkers = sortedTopTalkers.slice(0, 10);
        // Convert topTenTalkers array to separate arrays for Plotly.js
        var talkerKeys = topTenTalkers.map(entry => entry[0]);
        var talkerValues = topTenTalkers.map(entry => entry[1]);

        // Update Top Talkers Bar Graph
        Plotly.newPlot('topTalkers', [{
            type: 'bar',
            x: talkerKeys,    // IP addresses on the x-axis
            y: talkerValues,  // Number of packets on the y-axis
            marker: {
                color: 'green',  // You can customize the color if needed
            },
        }]);
    });



    function updateChart() {
        // Update the chart with accumulated data
        Plotly.update('throughputGraph', { x: [xValues], y: [yValues] });
    }

    socket.on('update_throughput', function (data) {
        // Update Throughput Over Time Line Graph with formatted timestamps
        var formattedTime = data.time.map(timestamp => {
            var unixTimestamp = parseFloat(timestamp);
            var date = new Date(unixTimestamp * 1000);
            var hours = date.getHours().toString().padStart(2, '0');
            var minutes = date.getMinutes().toString().padStart(2, '0');
            var seconds = date.getSeconds().toString().padStart(2, '0');
            return `${hours}:${minutes}:${seconds}`;
        });
        //console.log(formattedTime)
    
        // Accumulate data
        xValues.push(...formattedTime);
        yValues.push(...data.throughput);
    
        // Update data arrays with new values
        if (xValues.length > 1) {
            var lastTimestamp = new Date(xValues[xValues.length - 1]);
            var secondLastTimestamp = new Date(xValues[xValues.length - 2]);
    
            // Compare minutes and seconds
            if (
                lastTimestamp.getMinutes() !== secondLastTimestamp.getMinutes() ||
                lastTimestamp.getSeconds() !== secondLastTimestamp.getSeconds()
            ) {
                // If a minute or second has passed, update the chart
                updateChart();
            }
        }
    });
    
});
