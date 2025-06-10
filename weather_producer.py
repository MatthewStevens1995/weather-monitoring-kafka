# weather_producer.py
from kafka import KafkaProducer
import json
import time
import random
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherSensor:
    def __init__(self, sensor_id, location):
        self.sensor_id = sensor_id
        self.location = location
        # Base temperature for the location (randomized for simulation)
        self.base_temp = random.uniform(5.0, 30.0)
    
    def get_temperature(self):
        # Simulate temperature fluctuation around base temperature
        fluctuation = random.uniform(-2.0, 2.0)
        return round(self.base_temp + fluctuation, 1)
    
    def generate_reading(self):
        """Generate a simulated weather reading."""
        timestamp = datetime.now().isoformat()
        temperature = self.get_temperature()
        humidity = random.uniform(30.0, 90.0)
        
        return {
            "sensor_id": self.sensor_id,
            "location": self.location,
            "timestamp": timestamp,
            "temperature": temperature,
            "humidity": round(humidity, 1),
            "weather_condition": self._get_weather_condition(temperature, humidity)
        }
    
    def _get_weather_condition(self, temp, humidity):
        """Determine weather condition based on temperature and humidity."""
        conditions = ["Sunny", "Cloudy", "Rainy", "Foggy", "Windy"]
        # Simple logic for demonstration purposes
        if temp > 25 and humidity < 60:
            return "Sunny"
        elif temp < 10:
            return "Windy"
        elif humidity > 80:
            return "Rainy"
        elif humidity > 70:
            return "Foggy"
        else:
            return "Cloudy"

def json_serializer(data):
    """Serialize json messages."""
    return json.dumps(data).encode('utf-8')

def create_producer():
    """Create and return a Kafka producer."""
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=json_serializer,
        acks='all',
        retries=3
    )

def run_simulation(producer, sensors, topic_name, interval=2):
    """Run the weather simulation, sending data from all sensors to Kafka."""
    try:
        while True:
            for sensor in sensors:
                reading = sensor.generate_reading()
                # Use location as key for partitioning
                key = sensor.location.encode('utf-8')
                
                # Send the reading to Kafka
                future = producer.send(topic_name, key=key, value=reading)
                # Wait for the message to be sent
                record_metadata = future.get(timeout=10)
                
                logger.info(f"Sent reading from {sensor.location}: {reading['temperature']}°C, "
                           f"{reading['humidity']}% - {reading['weather_condition']}")
                logger.debug(f"Sent to partition {record_metadata.partition}, "
                            f"offset {record_metadata.offset}")
            
            # Wait before sending the next batch
            time.sleep(interval)
    except KeyboardInterrupt:
        logger.info("Simulation stopped by user")
    except Exception as e:
        logger.error(f"Error in simulation: {e}")
    finally:
        producer.flush()
        producer.close()
        logger.info("Producer closed")

if __name__ == "__main__":
    # Create sensors for different locations
    sensors = [
        WeatherSensor("sensor-001", "New York"),
        WeatherSensor("sensor-002", "London"),
        WeatherSensor("sensor-003", "Tokyo"),
        WeatherSensor("sensor-004", "Sydney"),
        WeatherSensor("sensor-005", "Rio de Janeiro"),
    ]
    
    # Create Kafka producer
    producer = create_producer()
    
    # Run the simulation
    run_simulation(producer, sensors, "weather-data")