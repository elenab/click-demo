import click


class Config(object):
    def __init__(self):
        self.verbose = False


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--verbose', is_flag=True)
@click.option('--home-directory', type=click.Path())
@pass_config
def cli(config, verbose, home_directory):
    if home_directory is None:
        home_directory = '.'
    config.home_directory = home_directory
    config.verbose = verbose


@cli.command()
@click.option('--string-to-print', default='world', help='The subject of the greeting.')
@click.option('--repeat', default=1, type=int, help='How many times you should be greeted.')
@click.argument('out', type=click.File('w'), default='-', required=False)
@pass_config
def greet(config, string_to_print, repeat, out):
    """
     This script is the Greeter.
    \b
    :param out: The file to write the greeting into. Defaults to '-'.
    """

    click.echo(f'Home directory is {config.home_directory}')
    if config.verbose:
        click.echo('We are in verbose mode')

    click.echo_via_pager('\n'.join('Line %d' % idx
                                   for idx in range(60)))
    click.clear()

    click.secho('\nOne fish ', bold=True, nl=False)
    click.secho('Two fish', underline=True, nl=False)
    click.secho(' Red fish ', fg='red', nl=False)
    click.secho('Blue fish\n', fg='blue', nl=False)

    for x in range(repeat):
        click.echo(f'Hello {string_to_print}!', file=out)
