import re

SERVICE_PATTERNS = {
    "postgres": [
        "could not connect to server",
        "connection refused",
        "psycopg2",
        "postgres://",
        "org.postgresql.util.PSQLException"
    ],
    "redis": [
        "redis.exceptions.ConnectionError",
        "ECONNREFUSED 127.0.0.1:6379",
        "ioredis",
        "redis://"
    ],
    "mongodb": [
        "MongooseServerSelectionError",
        "localhost:27017",
        "mongodb://",
        "com.mongodb.MongoTimeoutException"
    ],
    "mysql": [
        "Access denied for user",
        "Can't connect to MySQL server",
        "mysql://",
        "com.mysql.cj.jdbc.exceptions"
    ],
    "elasticsearch": [
        "NoNodeAvailableException",
        "elasticsearch://",
        "Connection refused.*9200"
    ],
    "rabbitmq": [
        "amqp://",
        "pika.exceptions.AMQPConnectionError",
        "ECONNREFUSED.*5672"
    ],
    "kafka": [
        "BrokerTransportFailure",
        "kafka://",
        "Connection refused.*9092"
    ],
    "memcached": [
        "memcached://",
        "MemcachedConnectionError"
    ],
    "mariadb": [
        "mariadb://"
    ],
    "neo4j": [
        "neo4j://",
        "bolt://"
    ]
}

def detect_services(logs: str) -> list[str]:
    """
    Detect missing services from logs.
    Returns a list of service names detected.
    """
    if not logs:
        return []
        
    detected = set()
    logs_lower = logs.lower()
    
    for service, patterns in SERVICE_PATTERNS.items():
        for pattern in patterns:
            # We use lower case matching
            # And support simple string matching or regex if needed
            if pattern.lower() in logs_lower or re.search(pattern, logs, re.IGNORECASE):
                detected.add(service)
                break
                
    # If kafka is detected, we typically also need zookeeper
    if "kafka" in detected:
        detected.add("zookeeper")
        
    return list(detected)
