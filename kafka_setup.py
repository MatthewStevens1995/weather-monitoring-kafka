# kafka_setup.py
from kafka.admin import KafkaAdminClient, NewTopic
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_topic(topic_name, num_partitions=3, replication_factor=1):
    """Create a Kafka topic if it doesn't exist."""
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=['localhost:9092'],
            client_id='weather-admin'
        )
        
        # Check if topic already exists
        existing_topics = admin_client.list_topics()
        if topic_name in existing_topics:
            logger.info(f"Topic '{topic_name}' already exists")
            return
        
        # Create new topic
        topic = NewTopic(
            name=topic_name,
            num_partitions=num_partitions,
            replication_factor=replication_factor
        )
        admin_client.create_topics([topic])
        logger.info(f"Topic '{topic_name}' created successfully")
    except Exception as e:
        logger.error(f"Error creating topic: {e}")
    finally:
        if 'admin_client' in locals():
            admin_client.close()

if __name__ == "__main__":
    create_topic("weather-data")