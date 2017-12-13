## Command line applications with Click

  Click is a Python package for creating command line interfaces
  in a composable way with as little code as necessary.  It's the "Command
  Line Interface Creation Kit".  It's highly configurable and it comes with
  sensible defaults out of the box.

  It aims to make the process of writing command line tools quick and fun.

  Click in three points:

  -   arbitrary nesting of commands
  -   automatic help page generation
  -   supports lazy loading of subcommands at runtime


Click was written to support the Flask microframework ecosystem because no tool could provide it with the functionality it needed.
To the best of the developer’s knowledge, Click is the first Python library that aims to create a level of composability of applications that goes beyond what the system itself supports.

## Why Click?
- is lazily composable without restrictions
- fully follows the Unix command line conventions
- supports loading values from environment variables out of the box
- supports for prompting of custom values
- is fully nestable and composable
- works the same in Python 2 and 3
- supports file handling out of the box
- comes with useful common helpers (getting terminal dimensions, ANSI colors, fetching direct keyboard input, screen clearing, finding config paths, launching apps and editors, etc.)

###Click aims to support fully composable command line user interfaces by doing the following:
- Click does not just parse, it also dispatches to the appropriate code.
- Click has a strong concept of an invocation context that allows subcommands to respond to data from the parent command.
- Click has strong information available for all parameters and commands so that it can generate unified help pages for the full CLI and to assist the user in converting the input data as necessary.
- Click has a strong understanding of what types are and can give the user consistent error messages if something goes wrong. A subcommand written by a different developer will not suddenly die with a different error messsage because it’s manually handled.
- Click has enough meta information available for its whole program that it can evolve over time to improve the user experience without forcing developers to adjust their programs. For instance, if Click decides to change how help pages are formatted, all Click programs will automatically benefit from this.


##Installation
It is highly recommended using a virtualenv.
When writing command line utilities, it’s recommended to write them as modules that are distributed with setuptools instead of using Unix shebangs.

This will help to use the python module we are writing as a command line tool.
To bundle your script with setuptools, all you need is the script in a Python package and a setup.py file.

Imagine this directory structure:

    hello.py
    setup.py

Contents of hello.py:

```import click

@click.command()
def cli():
    """Example script."""
    click.echo('Hello World!')
```    
Contents of setup.py:
 
```from setuptools import setup

setup(
    name="HelloWorld",
    version='1.0',
    py_modules=['hello'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        hello=hello:cli
    ''',
)
```

The magic is in the _entry_points_ parameter. Below _console_scripts_, each line identifies one console script. The first part before the equals sign (=) is the name of the script that should be generated, the second part is the import path followed by a colon (:) with the Click command.

That’s it.


###Testing The Script
To test the script, you can make a new virtualenv and then install your package:

```
$ virtualenv venv
$ . venv/bin/activate
$ pip install --editable .

```
Afterwards, your command should be available:

```
$ hello
Hello World!

$ hello --help
Usage: hello [OPTIONS]

Options:
--help  Show this message and exit.

```

### Standard options and arguments:

An option is optional and it starts with `--` or `-`.  
Arguments come after options and are mandatory. 
Arguments cannot have help text, they should be documented as part of the function docstring. Arguments are very specific, unlike options.


Click types, which are a bit more powerful and customizes how click interacts with this value. 
For example, if we define a click file type, this file is opened lazy by default. 
It will only be created as you write into the file.



```
@click.option('--string', default='World', help='The string to greet.')
@click.option('--repeat', default=1, help='How many times to greet.')
@click.argument('out', type=click.File('w'), default='-', required=False)
def greet(string, repeat, out):
    '''
    Greets a message.
    '''
    for i in range(repeat):
        click.echo(f'Hello {string}!', file=out)
```

Click automatically derives the type of the parameter from the default type.

If no default value is provided, they are assumed to be strings
You can be explicit and add the type, for example ```type=int```.


If we pass an invalid value, we get an error.
```
$ hello --string=Elementals --repeat=aaaq
Usage: greet [OPTIONS] [OUT]

Error: Invalid value for "--repeat": aaaq is not a valid integer
```

##Callback Invocation
For a regular command, the callback is executed whenever the command runs. If the script is the only command, it will always fire (unless a parameter callback prevents it. This for instance happens if someone passes --help to the script).

For groups, the situation looks different. In this case, the callback fires whenever a subcommand fires (unless this behavior is changed). What this means in practice is that an outer command runs when an inner command runs:
How to communicate data from the group to the subcommand? 
The answer to this is to use the click context:
```
import click

class Config(object):
    def __init__(self):
        self.verbose = False

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--verbose', is_flag=True)
@pass_config
def cli(config, verbose):
    if verbose:
        config.verbose = verbose

    pass

@cli.command()
@click.option('--string', default='World', help='The string to greet.')
@click.option('--repeat', default=1, help='How many times to greet.')
@click.argument('out', type=click.File('w'), default='-', required=False)
@pass_config
def greet(config, string, repeat, out):
    '''
    Greets a message.
    '''

    if config.verbose:
        click.echo('We are in verbose mode...')
    for i in range(repeat):
        click.echo(f'Hello {string}!', file=out)
```

```click.group``` decorator works exactly as the ```click.command```, the difference is that any group can have subcommands.
It is a very useful concept for building complex application.

###Other Click features:
 - Values from Environment Variables
 - Range Options
 - Choice Options
 - Variadic Arguments - if nargs parameter is set to -1, then an unlimited number of arguments is accepted
 - User Input prompts
 - Password Prompts
 - Custom Types -  subclassing the ParamType class
 - Multi Command Chaining
 - Multi Command Pipelines
 - CliRunner (testing)
 - Pager support
 - Launching editors, applications
 - etc..
 
## References:
 - [About Click](http://click.pocoo.org/5/)
 - [Building command line applications with Click](http://pymbook.readthedocs.io/en/latest/click.html)
 - [Click repo in github](https://github.com/pallets/click)
 - [Click Advanced Patterns](http://click.pocoo.org/5/advanced/)
 - [Testing Click Aplications](http://click.pocoo.org/5/testing/)
 - [Clicl Api Reference](http://click.pocoo.org/5/api/)
 - [Setuptools Integration](http://click.pocoo.org/5/setuptools/#setuptools-integration)
 - [Virtualenv and pip Basics](http://jonathanchu.is/posts/virtualenv-and-pip-basics/)
  
