from app.detector.error_parser import detect_services

def test_detect_services_postgres():
    logs = "Error: could not connect to server: Connection refused"
    result = detect_services(logs)
    
    assert "postgres" in result
    assert len(result) == 1

def test_detect_services_redis():
    logs = "redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379"
    result = detect_services(logs)
    
    assert "redis" in result
    assert len(result) == 1

def test_detect_services_kafka():
    logs = "BrokerTransportFailure: connection timeout to node 0"
    result = detect_services(logs)
    
    assert "kafka" in result
    assert "zookeeper" in result # zookeeper is added automatically
    assert len(result) == 2

def test_detect_services_multiple():
    logs = '''
    mongooseServerSelectionError: connect ECONNREFUSED 127.0.0.1:27017
    redis.exceptions.ConnectionError: Error 111
    '''
    result = detect_services(logs)
    
    assert "mongodb" in result
    assert "redis" in result
    assert len(result) == 2

def test_detect_services_empty():
    result = detect_services("")
    assert result == []

def test_detect_services_unmatched():
    logs = "Some random error that doesn't match any service"
    result = detect_services(logs)
    assert result == []
