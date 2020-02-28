import click
from flask.cli import AppGroup

test_cli = AppGroup("tester")


def configure_test_commands(app):
    app.cli.add_command(test_cli)


@test_cli.command("word")
@click.argument("word")
def print_word(word):
    from flask import current_app
    print(f"Printing {word}")
    current_app.logger.info(f"Logging {word}")
