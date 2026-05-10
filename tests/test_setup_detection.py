from app.services.detector import detect_stack

def test_detect_stack_node(tmp_path):
    (tmp_path / "package.json").write_text("{}")

    result = detect_stack(str(tmp_path))

    assert "Node.js" in result
    assert len(result) == 1

def test_detect_stack_python(tmp_path):
    (tmp_path / "requirements.txt").write_text("")

    result = detect_stack(str(tmp_path))

    assert "Python" in result
    assert len(result) == 1

def test_detect_stack_multiple(tmp_path):
    (tmp_path / "package.json").write_text("{}")
    (tmp_path / "Dockerfile").write_text("")

    result = detect_stack(str(tmp_path))

    assert "Node.js" in result
    assert "Docker" in result
    assert len(result) == 2

def test_detect_stack_empty(tmp_path):
    result = detect_stack(str(tmp_path))

    assert result == []