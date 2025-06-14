# llm-tools-docker

[![PyPI](https://img.shields.io/pypi/v/llm-tools-docker.svg)](https://pypi.org/project/llm-tools-docker/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-tools-docker?include_prereleases&label=changelog)](https://github.com/simonw/llm-tools-docker/releases)
[![Tests](https://github.com/simonw/llm-tools-docker/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-tools-docker/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-tools-docker/blob/main/LICENSE)

Run commands in a Docker container via an LLM tool

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-tools-docker
```
## Usage

To use this with the [LLM command-line tool](https://llm.datasette.io/en/stable/usage.html):

```bash
llm chat -T DockerAlpine --tools-debug --chain-limit 0
```
Then in the chat try:

> `Install Python 3 and use it to draw a cowsay cow`

This plugin currently only works with `llm chat` since the container is not persisted across multiple calls.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-tools-docker
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
