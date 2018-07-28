#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `plonecli` package."""

from click.testing import CliRunner
from plonecli import cli

import click
import os
import pytest
import subprocess


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    # assert 'Plone Command Line Interface' in result.output

    help_result = runner.invoke(cli.cli, ['--help'])
    assert help_result.exit_code == 0
    assert 'Usage: cli' in help_result.output

    help_result = runner.invoke(cli.cli, ['-h'])
    assert help_result.exit_code == 0
    assert 'Usage: cli' in help_result.output

    version_result = runner.invoke(cli.cli, ['-V'])
    assert version_result.exit_code == 0
    assert 'Available packages:' in version_result.output

    version_result = runner.invoke(cli.cli, ['--versions'])
    assert version_result.exit_code == 0
    assert 'Available packages:' in version_result.output


def test_plonecli_test():
    runner = CliRunner()
    template = """[main]
version = 5.1-latest
template = plone_addon
git_init = y
"""
    with runner.isolated_filesystem():
        with open('bobtemplate.cfg', 'w') as f:
            f.write(template)

        context = click.Context(cli.run_test)
        context.obj = {}
        context.obj['target_dir'] = os.path.dirname(
            os.path.abspath('bobtemplate.cfg'),
        )

        test_command_result_a = runner.invoke(
            cli.run_test, args=['--all'],
            obj=context.obj,
        )
        assert u'\nRUN: ./bin/test --all' in test_command_result_a.output

        test_command_result_t_a = runner.invoke(
            cli.run_test,
            args=['-t src/collective/todo/tests/test_robot.py', '-a'],
            obj=context.obj,
        )
        assert u'./bin/test --test  src/collective/todo/tests/test_robot.py --all' in test_command_result_t_a.output  # NOQA: E501

        test_command_result_s_a = runner.invoke(
            cli.run_test,
            args=['-s collective.todo', '-a'],
            obj=context.obj,
        )
        assert u'./bin/test --package  collective.todo --all' in test_command_result_s_a.output  # NOQA: E501

        test_command_result_t_s = runner.invoke(
            cli.run_test,
            args=[
                '-t src/collective/todo/tests/test_robot.py',
                '-s collective.todo'
            ],
            obj=context.obj,
        )
        assert u'./bin/test --test  src/collective/todo/tests/test_robot.py --package  collective.todo' in test_command_result_t_s.output  # NOQA: E501

        test_command_result = runner.invoke(
            cli.run_test,
            args=[
                '-t src/collective/todo/tests/test_robot.py',
                '-s collective.todo',
                '--all'
            ],
            obj=context.obj,
        )
        assert u'./bin/test --test  src/collective/todo/tests/test_robot.py --package  collective.todo --all' in test_command_result.output  # NOQA: E501
