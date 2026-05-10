SERVICE_CONFIG = {
    "postgres": {
        "image": "postgres:15",
        "ports": ["5432:5432"],
        "env": {
            "POSTGRES_USER": "user",
            "POSTGRES_PASSWORD": "password",
            "POSTGRES_DB": "app_db"
        }
    },
    "redis": {
        "image": "redis:7",
        "ports": ["6379:6379"],
        "env": {}
    },
    "mongodb": {
        "image": "mongo:6",
        "ports": ["27017:27017"],
        "env": {}
    },
    "mysql": {
        "image": "mysql:8",
        "ports": ["3306:3306"],
        "env": {
            "MYSQL_ROOT_PASSWORD": "password",
            "MYSQL_DATABASE": "app_db",
            "MYSQL_USER": "user",
            "MYSQL_PASSWORD": "password"
        }
    },
    "elasticsearch": {
        "image": "docker.elastic.co/elasticsearch/elasticsearch:8.10.2",
        "ports": ["9200:9200", "9300:9300"],
        "env": {
            "discovery.type": "single-node",
            "xpack.security.enabled": "false"
        }
    },
    "rabbitmq": {
        "image": "rabbitmq:3-management",
        "ports": ["5672:5672", "15672:15672"],
        "env": {}
    },
    "kafka": {
        "image": "confluentinc/cp-kafka:7.3.0",
        "ports": ["9092:9092"],
        "env": {
            "KAFKA_ZOOKEEPER_CONNECT": "zookeeper:2181",
            "KAFKA_ADVERTISED_LISTENERS": "PLAINTEXT://localhost:9092",
            "KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR": "1"
        }
    },
    "zookeeper": {
        "image": "confluentinc/cp-zookeeper:7.3.0",
        "ports": ["2181:2181"],
        "env": {
            "ZOOKEEPER_CLIENT_PORT": "2181",
            "ZOOKEEPER_TICK_TIME": "2000"
        }
    },
    "memcached": {
        "image": "memcached:1.6",
        "ports": ["11211:11211"],
        "env": {}
    },
    "mariadb": {
        "image": "mariadb:10",
        "ports": ["3306:3306"],
        "env": {
            "MARIADB_ROOT_PASSWORD": "password",
            "MARIADB_DATABASE": "app_db",
            "MARIADB_USER": "user",
            "MARIADB_PASSWORD": "password"
        }
    },
    "neo4j": {
        "image": "neo4j:5",
        "ports": ["7474:7474", "7687:7687"],
        "env": {
            "NEO4J_AUTH": "neo4j/password"
        }
    }
}
