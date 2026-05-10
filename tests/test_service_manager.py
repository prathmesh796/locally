from unittest.mock import patch, MagicMock
from app.orchestrator.service_manager import pre_detect_services, process_services, handle_missing_services

def test_pre_detect_services_env(tmp_path):
    (tmp_path / ".env").write_text("POSTGRES_USER=test\nREDIS_URL=test")
    
    result = pre_detect_services(str(tmp_path))
    
    assert "postgres" in result
    assert "redis" in result

def test_pre_detect_services_package_json(tmp_path):
    (tmp_path / "package.json").write_text('{"dependencies": {"mongoose": "^6.0.0", "kafkajs": "^2.0.0"}}')
    
    result = pre_detect_services(str(tmp_path))
    
    assert "mongodb" in result
    assert "kafka" in result
    assert "zookeeper" in result # zookeeper is added automatically when kafka is present

@patch("app.orchestrator.service_manager.check_docker_installed")
@patch("app.orchestrator.service_manager.ensure_docker_running")
@patch("app.orchestrator.service_manager.generate_compose")
@patch("app.orchestrator.service_manager.run_compose")
@patch("app.orchestrator.service_manager.wait_for_services")
@patch("app.orchestrator.service_manager.Confirm.ask")
def test_process_services_success(mock_ask, mock_wait, mock_run, mock_gen, mock_ensure, mock_check):
    mock_ask.return_value = True
    mock_check.return_value = True
    mock_ensure.return_value = True
    mock_gen.return_value = "docker-compose.generated.yml"
    mock_run.return_value = True
    
    result = process_services(["postgres", "redis"], "/target/path")
    
    assert result is True
    mock_ask.assert_called_once()
    mock_check.assert_called_once()
    mock_ensure.assert_called_once()
    mock_gen.assert_called_once_with(["postgres", "redis"], "/target/path")
    mock_run.assert_called_once_with("docker-compose.generated.yml", "/target/path")
    mock_wait.assert_called_once_with(["postgres", "redis"])

@patch("app.orchestrator.service_manager.check_docker_installed")
@patch("app.orchestrator.service_manager.Confirm.ask")
def test_process_services_no_docker(mock_ask, mock_check):
    mock_ask.return_value = True
    mock_check.return_value = False
    
    result = process_services(["postgres"], "/target/path")
    
    assert result is False
    mock_ask.assert_called_once()
    mock_check.assert_called_once()

@patch("app.orchestrator.service_manager.detect_services")
@patch("app.orchestrator.service_manager.process_services")
def test_handle_missing_services(mock_process, mock_detect):
    mock_detect.return_value = ["mysql"]
    mock_process.return_value = True
    
    result = handle_missing_services("Error: Can't connect to MySQL server", "/target/path")
    
    assert result is True
    mock_detect.assert_called_once_with("Error: Can't connect to MySQL server")
    mock_process.assert_called_once_with(["mysql"], "/target/path", ask_permission=True)