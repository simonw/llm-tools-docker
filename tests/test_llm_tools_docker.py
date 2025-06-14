from click.testing import CliRunner
import llm.cli


def test_tool():
    runner = CliRunner()
    result = runner.invoke(llm.cli.cli, ["tools"])
    assert result.exit_code == 0
    assert "DockerAlpine" in result.output
