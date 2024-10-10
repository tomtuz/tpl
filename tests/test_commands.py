from unittest.mock import MagicMock, patch

import pytest
from src.core.commands import cmd_config, cmd_plugin, cmd_spawn, cmd_template


@pytest.fixture
def mock_logger():
    with patch("src.core.commands.logger") as mock:
        yield mock


class TestCommands:
    def test_cmd_config_get(self, mock_logger):
        with patch("src.core.commands.get_config_value") as mock_get:
            mock_get.return_value = "test_value"
            cmd_config(["get", "test_key"])
            mock_get.assert_called_once_with("test_key")
            mock_logger.info.assert_called()

    def test_cmd_config_set(self, mock_logger):
        with patch("src.core.commands.set_config_value") as mock_set:
            cmd_config(["set", "test_key", "test_value"])
            mock_set.assert_called_once_with("test_key", "test_value")
            mock_logger.info.assert_called()

    def test_cmd_config_remove(self, mock_logger):
        with patch("src.core.commands.remove_config_value") as mock_remove:
            cmd_config(["remove", "test_key"])
            mock_remove.assert_called_once_with("test_key")
            mock_logger.info.assert_called()

    def test_cmd_config_invalid_action(self, mock_logger):
        with pytest.raises(ValueError):
            cmd_config(["invalid_action", "test_key"])

    def test_cmd_spawn_with_args(self, mock_logger):
        with patch("src.core.commands.log") as mock_log:
            cmd_spawn(["test_file", "test_variant"])
            mock_log.assert_called_once_with("spawn", ["filename", "variant"], ["test_file", "test_variant"])
            mock_logger.info.assert_called()

    def test_cmd_spawn_without_args(self, mock_logger):
        with patch("src.core.commands.cli_selector_spawn") as mock_selector:
            cmd_spawn([])
            mock_selector.assert_called_once()
            mock_logger.info.assert_called()

    def test_cmd_template(self, mock_logger):
        with patch("src.core.commands.importlib.util.spec_from_file_location") as mock_spec:
            mock_module = MagicMock()
            mock_spec.return_value.loader.exec_module.return_value = None
            mock_spec.return_value.loader.exec_module.side_effect = lambda m: setattr(m, "run", MagicMock())
            with patch("src.core.commands.os.path.exists", return_value=True):
                cmd_template(["test_template", "test_command", "option1", "option2"])
                mock_module.run.assert_called_once_with(["option1", "option2"])
                mock_logger.info.assert_called()

    def test_cmd_template_invalid_template(self, mock_logger):
        with patch("src.core.commands.os.path.exists", return_value=False):
            with pytest.raises(ValueError):
                cmd_template(["invalid_template", "test_command"])

    def test_cmd_plugin_list(self, mock_logger):
        with patch("src.core.commands.list_plugins", return_value=["plugin1", "plugin2"]):
            cmd_plugin([])
            mock_logger.info.assert_called()

    def test_cmd_plugin_run(self, mock_logger):
        mock_plugin = MagicMock()
        with patch("src.core.commands.get_plugin", return_value=mock_plugin):
            cmd_plugin(["test_plugin", "option1", "option2"])
            mock_plugin.run.assert_called_once_with(["option1", "option2"])
            mock_logger.info.assert_called()

    def test_cmd_plugin_invalid(self, mock_logger):
        with patch("src.core.commands.get_plugin", return_value=None):
            with pytest.raises(ValueError):
                cmd_plugin(["invalid_plugin"])


if __name__ == "__main__":
    pytest.main()
