# Real-Time Weather Monitoring System with Apache Kafka

A distributed weather data processing system that demonstrates real-time event streaming using Apache Kafka. This project simulates multiple weather sensors sending data to a central processing application for analysis and alert generation.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Apache Kafka](https://img.shields.io/badge/apache%20kafka-2.13_%7C_3.0-orange.svg)](https://kafka.apache.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Real-time Data Streaming**: Continuous weather data streaming from multiple simulated sensors
- **Apache Kafka Integration**: Demonstration of Kafka producers, consumers, and topic management
- **Data Processing**: Real-time analysis including average temperature calculations and weather condition determination
- **Alert System**: Automatic alerts for extreme temperature conditions (>30°C or <0°C)
- **Geographical Partitioning**: Location-based message partitioning for efficient data organization
- **Educational Value**: Clean, well-documented code ideal for learning event-driven architectures

## Architecture

```
Weather Sensors → Kafka Topic → Weather Analyzer
    (Producer)    ("weather-data")    (Consumer)
```

## Prerequisites

- Python 3.8+
- Apache Kafka 2.13+ or Docker
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MatthewStevens1995/weather-monitoring-kafka.git
   cd weather-monitoring-kafka
   ```

2. **Set up Kafka with Docker**
   ```bash
   # Start Kafka and Zookeeper
   docker-compose up -d
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
weather-monitoring-kafka/
├── kafka_setup.py      # Topic creation utility
├── weather_producer.py # Sensor data simulation
├── weather_consumer.py # Data processing and analysis
├── requirements.txt    # Python dependencies
├── docker-compose.yml  # Kafka infrastructure
└── README.md
```

## Usage

### 1. Create Kafka Topic
```bash
python kafka_setup.py
```

### 2. Start the Weather Producer
```bash
python weather_producer.py
```

### 3. Start the Weather Consumer
```bash
python weather_consumer.py
```

## Configuration

### Modifying Sensor Locations
Edit the `weather_producer.py` file to add or modify sensor locations:

```python
sensors = [
    WeatherSensor("sensor-001", "New York"),
    WeatherSensor("sensor-002", "London"),
    # Add your locations here
]
```

### Adjusting Alert Thresholds
Modify temperature thresholds in `weather_consumer.py`:

```python
if temperature > 30:  # High temperature alert
    # Alert logic here
elif temperature < 0:  # Low temperature alert
    # Alert logic here
```

## Example Output

### Producer Output
```
INFO:__main__:Sent reading from New York: 22.6°C, 62.3% - Cloudy
INFO:__main__:Sent reading from London: 14.1°C, 78.5% - Foggy
INFO:__main__:Sent reading from Tokyo: 25.3°C, 55.2% - Sunny
```

### Consumer Output
```
INFO:__main__:STATISTICS for New York:
INFO:__main__:  Average Temperature: 21.5°C
INFO:__main__:  Current Temperature: 22.6°C
INFO:__main__:  Current Humidity: 62.3%
INFO:__main__:  Current Condition: Cloudy
INFO:__main__:  Total Readings: 10
INFO:__main__:--------------------------------------------------
```

## Extending the Project

This project can be extended with:

1. **Database Integration**: Store readings in PostgreSQL or MongoDB
2. **Web Dashboard**: Create real-time visualizations with Flask/React
3. **Machine Learning**: Add prediction models for weather forecasting
4. **Multiple Consumers**: Implement different types of analytics
5. **Authentication**: Add security layers for production deployment

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError for kafka.vendor.six.moves**
   - Solution: Use the latest kafka-python version or the git development version:
   ```bash
   pip install git+https://github.com/dpkp/kafka-python.git
   ```

2. **Connection Refused Error**
   - Ensure Kafka and Zookeeper are running:
   ```bash
   docker-compose ps
   ```

3. **Topic Already Exists**
   - This is normal, the setup script checks for existing topics

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Learning Resources

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [kafka-python Documentation](https://kafka-python.readthedocs.io/)
- [Understanding Event-Driven Architecture](https://microservices.io/patterns/data/event-driven-architecture.html)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Apache Kafka community for excellent documentation
- The kafka-python maintainers for the Python client library
- Weather data simulation based on common meteorological patterns
- To all the people who supported me to get to where I am in life!

