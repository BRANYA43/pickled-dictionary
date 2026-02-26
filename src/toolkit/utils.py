import click


def slugify(value: str) -> str:
    return value.replace(' ', '_')


def info(text: str) -> str:
    return click.style(text, fg='blue')


def warning(text: str) -> str:
    return click.style(text, fg='yellow')


def success(text: str) -> str:
    return click.style(text, fg='green')


def danger(text: str) -> str:
    return click.style(text, fg='red')
