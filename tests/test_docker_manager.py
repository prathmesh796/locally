from unittest.mock import patch, mock_open
import subprocess
import os
from app.services.docker_manager import check_docker_installed, ensure_docker_running, generate_compose, run_compose

@patch("shutil.which")
@patch("subprocess.run")
def test_check_docker_installed_success(mock_run, mock_which):
    mock_which.return_value = "/usr/bin/docker"
    mock_run.return_value.returncode = 0
    
    assert check_docker_installed() is True

@patch("shutil.which")
def test_check_docker_installed_no_docker(mock_which):
    mock_which.return_value = None
    
    assert check_docker_installed() is False

@patch("subprocess.run")
def test_ensure_docker_running_already_running(mock_run):
    mock_run.return_value.returncode = 0
    
    assert ensure_docker_running() is True

@patch("app.services.docker_manager.platform.system")
@patch("subprocess.run")
@patch("time.sleep")
def test_ensure_docker_running_needs_start_mac(mock_sleep, mock_run, mock_system):
    mock_system.return_value = "darwin"
    
    # First call to `docker info` fails, second (to start) succeeds, third (retry) succeeds
    mock_run.side_effect = [
        subprocess.CalledProcessError(1, "cmd"),
        None, # open -a Docker
        None  # docker info inside the wait loop
    ]
    
    assert ensure_docker_running() is True
    assert mock_run.call_count == 3

@patch("builtins.open", new_callable=mock_open)
def test_generate_compose(mock_file):
    services = ["postgres", "redis"]
    target_path = "/tmp/fake_path"
    
    compose_path = generate_compose(services, target_path)
    
    assert compose_path == os.path.join(target_path, "docker-compose.generated.yml")
    mock_file.assert_called_once_with(compose_path, "w")
    
    # Check that it wrote yaml containing the images
    written_content = "".join([call.args[0] for call in mock_file().write.call_args_list])
    assert "postgres:15" in written_content
    assert "redis:7" in written_content
    assert "5432:5432" in written_content
    assert "6379:6379" in written_content

@patch("subprocess.run")
def test_run_compose_success(mock_run):
    # mock version check success
    mock_run.side_effect = [
        subprocess.CompletedProcess(args=["docker", "compose", "version"], returncode=0),
        subprocess.CompletedProcess(args=["docker", "compose", "-f", "compose.yml", "up", "-d"], returncode=0)
    ]
    
    assert run_compose("compose.yml", "/target") is True
    assert mock_run.call_count == 2
