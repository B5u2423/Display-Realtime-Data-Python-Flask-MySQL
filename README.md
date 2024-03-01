<a id="readme-top"></a>

# Display Realtime Data With Python, Flask and MySQL

## About

A simple system with 2 servers: a HTTP server for handling the data from the IoT devices, and a WebSocket server for sending real-time data to the client, which then will render the chart accordingly.

![System Overview](/assets/system-overview.png)
*An overview of the system.*

![Example Chart](/assets/rt-chart.png)
*The rendered real-time data page.*

## Built With

This project is built with all the following frameworks/libraries/plugins:

* [Flask](https://flask.palletsprojects.com/en/3.0.x/)
* [JQuery](https://jquery.com/)
* [ChartJS](https://www.chartjs.org/)
* [DataTables](https://datatables.net/)
* [SocketIO](https://socket.io/)

## Getting Started

### Prerequisites

You MUST have Python, Flask and MySQL installed, if not, Google how to. Most of the required Python libraries are noted the `requirement.txt` file, so run the following command to automatically install them:

```bash
pip install -r requirement.txt
```

### Installing

Just clone the repo and run. All the JavaScript libraries have been included in the `vendors` folder so the WebSocket server can be deployed locally without Internet connection.

```bash
git clone https://github.com/B5u2423/Display-Realtime-Data-Python-Flask-MySQL.git python-display-realtime
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Deployment

Run `http-server.py` if you want to receive data from the sensors and save it to the database. I use an ESP32 with a DHT11 sensor to gather data on temperature and humidity. The HTTP server is running on port `8090`, configure the URL according to your IP and the port in the device sketch. Example source code of the ESP32 is included the `sketch` folder.

Run `websock-server.py`, the WebSocket server is running on port `8091`, connect to it at `localhost:8091`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License - see [LICENSE](LICENSE) the for more details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
