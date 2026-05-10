import os
from unittest.mock import patch, MagicMock
from app.services.repo import clone_repo

@patch("app.services.repo.git.Repo.clone_from")
def test_clone_repo_success(mock_clone, tmp_path):
    target_path = str(tmp_path / "repo")
    
    result = clone_repo("https://github.com/test/repo.git", target_path)
    
    assert result is True
    mock_clone.assert_called_once_with("https://github.com/test/repo.git", target_path)

def test_clone_repo_existing_dir(tmp_path):
    # Create an existing directory with a file in it
    target_path = tmp_path / "existing_repo"
    target_path.mkdir()
    (target_path / "file.txt").write_text("hello")
    
    result = clone_repo("https://github.com/test/repo.git", str(target_path))
    
    assert result is True # Returns true because it skips cloning

@patch("app.services.repo.git.Repo.clone_from")
def test_clone_repo_failure(mock_clone, tmp_path):
    mock_clone.side_effect = Exception("Clone failed")
    target_path = str(tmp_path / "repo")
    
    result = clone_repo("https://github.com/test/repo.git", target_path)
    
    assert result is False
    mock_clone.assert_called_once()