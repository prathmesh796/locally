from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from app.cli.app import app
import os

runner = CliRunner()

def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Locally796" in result.stdout

@patch("app.cli.app.os.makedirs")
@patch("builtins.open")
def test_set_key(mock_open, mock_makedirs):
    result = runner.invoke(app, ["set-key", "fake-api-key"])
    assert result.exit_code == 0
    assert "API Key saved successfully" in result.stdout
    mock_makedirs.assert_called_once()
    mock_open.assert_called_once()

@patch("app.cli.app.clone_repo")
@patch("app.cli.app.detect_stack")
@patch("app.cli.app.run_setup_and_start")
def test_clone_and_run_success(mock_run, mock_detect, mock_clone):
    mock_clone.return_value = True
    mock_detect.return_value = ["python"]
    
    result = runner.invoke(app, ["clone-and-run", "https://github.com/test/repo"])
    
    assert result.exit_code == 0
    mock_clone.assert_called_once()
    mock_detect.assert_called_once()
    mock_run.assert_called_once()

@patch("app.cli.app.clone_repo")
def test_clone_and_run_failure(mock_clone):
    mock_clone.return_value = False
    
    result = runner.invoke(app, ["clone-and-run", "https://github.com/test/repo"])
    
    assert result.exit_code == 1
    assert "Aborting due to clone failure" in result.stdout