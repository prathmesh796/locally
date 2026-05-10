from unittest.mock import patch, MagicMock
from app.services.health_check import is_port_open, wait_for_services

@patch("socket.socket")
def test_is_port_open_success(mock_socket):
    mock_sock_instance = MagicMock()
    mock_sock_instance.connect_ex.return_value = 0
    mock_socket.return_value = mock_sock_instance
    
    assert is_port_open(5432) is True
    mock_sock_instance.connect_ex.assert_called_once_with(("127.0.0.1", 5432))

@patch("socket.socket")
def test_is_port_open_failure(mock_socket):
    mock_sock_instance = MagicMock()
    mock_sock_instance.connect_ex.return_value = 111 # Connection refused
    mock_socket.return_value = mock_sock_instance
    
    assert is_port_open(5432) is False

@patch("app.services.health_check.is_port_open")
@patch("time.sleep")
def test_wait_for_services_success(mock_sleep, mock_is_port_open):
    # Mock is_port_open to return True immediately
    mock_is_port_open.return_value = True
    
    # postgres needs 5432, redis needs 6379
    assert wait_for_services(["postgres", "redis"], timeout=5) is True
    
    # It should check both ports
    assert mock_is_port_open.call_count == 2
    mock_is_port_open.assert_any_call(5432)
    mock_is_port_open.assert_any_call(6379)

@patch("app.services.health_check.is_port_open")
@patch("time.sleep")
def test_wait_for_services_timeout(mock_sleep, mock_is_port_open):
    # Mock is_port_open to return False always, causing a timeout
    mock_is_port_open.return_value = False
    
    # We set a small timeout in the mock, wait_for_services loops every 2s
    # so we should mock time.time to advance
    with patch("time.time", side_effect=[0, 1, 3, 6, 6, 6, 6, 6]):
        assert wait_for_services(["postgres"], timeout=5) is False
