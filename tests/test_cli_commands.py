from src.main import app
from typer.testing import CliRunner

runner = CliRunner()


def test_tpl_no_args():
    result = runner.invoke(app)
    print(f"Exit code: {result.exit_code}")
    print(f"Output: {result.output}")
    assert result.exit_code == 0
    assert "Usage: " in result.output


def test_tpl_spawn_no_args():
    result = runner.invoke(app, ["spawn"])
    assert result.exit_code == 0
    # Add more specific assertions based on the expected behavior of spawn without arguments


def test_tpl_config_set():
    result = runner.invoke(app, ["config", "set", "test_key", "test_value"])
    assert result.exit_code == 0
    # Add more specific assertions based on the expected behavior of config set


def test_tpl_config_get():
    # First, set a value
    runner.invoke(app, ["config", "set", "test_key", "test_value"])
    # Then, get the value
    result = runner.invoke(app, ["config", "get", "test_key"])
    assert result.exit_code == 0
    assert "test_value" in result.output


def test_tpl_template():
    result = runner.invoke(app, ["template", "test_template", "test_command"])
    # The command might fail if the template doesn't exist, but it should still exit gracefully
    assert result.exit_code in [0, 1]
    if result.exit_code == 1:
        assert "Error:" in result.output


def test_tpl_plugin():
    result = runner.invoke(app, ["plugin", "test_plugin"])
    # The command might fail if the plugin doesn't exist, but it should still exit gracefully
    assert result.exit_code in [0, 1]
    if result.exit_code == 1:
        assert "Error:" in result.output

