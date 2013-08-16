## Documentation with *Sphinx*

[Sphinx](http://www.sphinx-doc.org) is a tool by the [pocoo](http://www.pocoo.org/) folks. It's used to 
generate the Python's official documentation and the documentation for almost all other popular Python 
packages. It was written with idea of making auto-generation of HTML documentation from 
Python code as easy as possible.

#### Let the tool do the work

Sphinx has no implicit knowledge of Python programs and how to extract
documentation from them. It only operates on reStructured Text files, which
means a reStructured Text version of your code's documentation needs to be
available for Sphinx to do its work. But maintaining a reStructured Text 
version of all of your `.py` files (minus the actual body of functions and
classes) is clearly not doable. Luckily, Sphinx has a javadoc-like extensions
which is able to create reStructured Text files from documentation extracted
from your code's docstrings.

!!!!!!!TODO!!!!!!!!!!

#### Installation

Be sure to install Sphinx *in your `virtualenv`*, since documentation will be a
versioned artifact in your project. Different versions of Sphinx may generate
different HTML output. By installing in your `virtualenv`, you can "upgrade" 
your documentation in a controlled manner.

We'll be keeping our documentation in the `docs` directory and the generated
documentation in the `docs/generated` directory. To auto-generate reStructured
Text documentation files from your `docstring`s, run the following command in
your project's root directory:

    #!bash
    $ sphinx-apidoc -F -o docs <package name>

This will create a `docs` directory with a number of documentation files. In
addition, it creates a `conf.py` file, which is responsible for configuration
of your documentation. You'll also see a `Makefile`, handy for building
HTML documentation in one command (`make html`).

Before you actually generate your documentation, be sure you've installed your
package locally (`$ python setup.py develop` is the easiest way to keep it up
to date, though you can use `pip` as well) or else `sphinx-apidoc` won't be able
to find your package.

#### Configuration: `conf.py`

The `conf.py` file that was created controls many aspects of the documentation
that's generated. It's well documented itself, so I'll briefly touch on just
two items. 

###### version and release

First, make sure to keep your `version` and `release` values 
up-to-date. Those numbers will be displayed as part of the generated
documentation, so you don't want them to drift from the actual values.

The easiest way to keep your version up to date, in both your documentation and
`setup.py` file, is to have it read from your package's `__version__`
attribute. I "borrowed" the following `conf.py` code for `sandman` from
Flask's `conf.py`:

    #!bash
    import pkg_resources
    try:
        release = pkg_resources.get_distribution('sandman').version
    except pkg_resources.DistributionNotFound:
        print 'To build the documentation, The distribution information of sandman'
        print 'Has to be available.  Either install the package into your'
        print 'development environment or run "setup.py develop" to setup the'
        print 'metadata.  A virtualenv is recommended!'
        sys.exit(1)
    del pkg_resources

    version = '.'.join(release.split('.')[:2])

This means that, to get the documentation to generate the correct version
number, you simply need to have run `$ python setup.py develop` in your
project's `virtualenv`. Now you only need to worry about keeping `__version__`
up to date, since `setup.py` makes use of it as well.

###### html_theme

Consider changing the `html_theme` from `default`. I'm partial 
to `nature`, obviously this is a matter of personal preference. The reason I
raise this point at all is because the official Python documentation changed
themes from `default` to `pydoctheme` between Python 2 and Python 3 (the latter
theme is a custom theme only available in the cPython source). To some people,
seeing the `default` theme makes a project seem "old".


