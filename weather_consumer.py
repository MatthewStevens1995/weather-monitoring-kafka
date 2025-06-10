# weather_consumer.py
from kafka import KafkaConsumer
import json
import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherAnalyzer:
    def __init__(self):
        # Store latest readings and statistics
        self.latest_readings = {}
        self.temperature_sums = defaultdict(float)
        self.reading_counts = defaultdict(int)
        self.temperature_alerts = set()
        
    def process_reading(self, reading):
        """Process a weather reading and update statistics."""
        location = reading['location']
        temperature = reading['temperature']
        
        # Update latest reading
        self.latest_readings[location] = reading
        
        # Update temperature statistics
        self.temperature_sums[location] += temperature
        self.reading_counts[location] += 1
        
        # Check for temperature alerts (above 30°C or below 0°C)
        if temperature > 30 and location not in self.temperature_alerts:
            logger.warning(f"HIGH TEMPERATURE ALERT: {location} has reached {temperature}°C!")
            self.temperature_alerts.add(location)
        elif temperature < 0 and location not in self.temperature_alerts:
            logger.warning(f"LOW TEMPERATURE ALERT: {location} has dropped to {temperature}°C!")
            self.temperature_alerts.add(location)
        elif 0 <= temperature <= 30 and location in self.temperature_alerts:
            # Remove from alerts if temperature returns to normal range
            self.temperature_alerts.remove(location)
            
        # Print statistics every 10 readings per location
        if self.reading_counts[location] % 10 == 0:
            self.print_statistics(location)
    
    def print_statistics(self, location):
        """Print statistics for a location."""
        if self.reading_counts[location] == 0:
            return
            
        avg_temp = self.temperature_sums[location] / self.reading_counts[location]
        logger.info(f"STATISTICS for {location}:")
        logger.info(f"  Average Temperature: {avg_temp:.1f}°C")
        logger.info(f"  Current Temperature: {self.latest_readings[location]['temperature']}°C")
        logger.info(f"  Current Humidity: {self.latest_readings[location]['humidity']}%")
        logger.info(f"  Current Condition: {self.latest_readings[location]['weather_condition']}")
        logger.info(f"  Total Readings: {self.reading_counts[location]}")
        logger.info("-" * 50)

def create_consumer(topic_name, group_id='weather-analyzers'):
    """Create and return a Kafka consumer."""
    return KafkaConsumer(
        topic_name,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=group_id,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

def run_consumer(topic_name):
    """Run the weather data consumer."""
    try:
        # Create consumer
        consumer = create_consumer(topic_name)
        analyzer = WeatherAnalyzer()
        
        logger.info(f"Starting consumer, listening for messages on '{topic_name}'...")
        
        # Process messages
        for message in consumer:
            reading = message.value
            logger.debug(f"Received: {reading}")
            analyzer.process_reading(reading)
            
    except KeyboardInterrupt:
        logger.info("Consumer stopped by user")
    except Exception as e:
        logger.error(f"Error in consumer: {e}")
    finally:
        if 'consumer' in locals():
            consumer.close()
            logger.info("Consumer closed")

if __name__ == "__main__":
    run_consumer("weather-data")