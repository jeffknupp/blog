## `setuptools` and the `setup.py` File

The `setup.py` file you've likely seen in other packages is used by the
`distutils` package for the installation of Python packages. It's an important
file for any project, as it contains information on versioning, package
requirements, the project description that will be used on PyPI, and your
name and contact information, among many other things. It allows packages to be
searched for an installed in a programmatic way, providing meta-data and
instructions to tools that do so.

The [`setuptools`](https://pythonhosted.org/setuptools/setuptools.html) package 
(really a set of enhancements for `distutils`) simplifies 
the building and distribution of Python packages. A Python package that was
packaged with `setuptools` should be indistinguishable from one packaged with
`distutils`. There's really no reason not to use it.

`setup.py` should live in your project's root directory. 
The most important section of `setup.py` is the call to `setuptools.setup`,
where all the meta-information about the package lives. Here's the complete
contents of `setup.py` from [sandman](http://www.github.com/jeffknupp/sandman):

    #!bash
    from __future__ import print_function
    from setuptools import setup, find_packages
    from setuptools.command.test import test as TestCommand
    import codecs
    import os
    import sys

    import sandman

    here = os.path.abspath(os.path.dirname(__file__))

    def read(*parts):
        return codecs.open(os.path.join(here, *parts), 'r').read()

    long_description = read('README.rst')

    class PyTest(TestCommand):
        def finalize_options(self):
            TestCommand.finalize_options(self)
            self.test_args = []
            self.test_suite = True

        def run_tests(self):
            import pytest
            errno = pytest.main(self.test_args)
            sys.exit(errno)

    setup(
        name='sandman',
        version=sandman.__version__,
        url='http://github.com/jeffknupp/sandman/',
        license='Apache Software License',
        author='Jeff Knupp',
        tests_require=['pytest'],
        install_requires=['Flask>=0.10.1',
                        'Flask-SQLAlchemy>=1.0',
                        'SQLAlchemy==0.8.2',
                        ],
        cmdclass={'test': PyTest},
        author_email='jeff@jeffknupp.com',
        description='Automated REST APIs for existing database-driven systems',
        long_description=long_description,
        packages=['sandman'],
        include_package_data=True,
        platforms='any',
        test_suite='sandman.test.test_sandman',
        classifiers = [
            'Programming Language :: Python',
            'Development Status :: 4 - Beta',
            'Natural Language :: English',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Libraries :: Application Frameworks',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            ],
        extras_require={
            'testing': ['pytest'],
        }
    )

Most of the contents are straightforward and could be gleaned from the
`setuptools` documentation, so I'll only touch on the "interesting" parts.
Using `sandman.__version__` and the method of getting `long_description` 
(taken from the `setup.py` of other projects, though I can't remember 
which ones) reduce the amount of boilerplate code we need to write. Instead 
of maintaining the project's version in three
places (`setup.py`, the package itself via `package.__version__`, and the
documentation), we can always use the package's version to populate the
`version` parameter in `setup`.

`long_description` is the document used by PyPI as the description on your 
project's PyPI page. As there is another file, `README.md` with almost the 
exact same content, I use [pandoc](http://johnmacfarlane.net/pandoc/) to
automatically generate `README.rst` from `README.md`. Thus, we can simply `read`
the file `README.rst` and use that as the value for `long_description`.

py.test (discussed below) has a special entry (`class PyTest`)
to allow `python setup.py test` to work correctly. That code snippet 
was taken directly from the `py.test` documentation.

Everything else is in the file is simply setting values for the `setup` 
parameters described in the documentation.

#### Other `setup.py` parameters

There are some `setup` arguments that [sandman](http://www.github.com/jeffknupp/sandman)
has no use for, but your package might. For example, you may be distributing
a script that you'd like your user to be able to execute from the command line.
In the example above, that script would only be installed in the normal
`site-packages` location along with the rest of your code. There would be no
(easy) way for the user to run it after it was installed.

For that reason, `setup` can take a `scripts` argument that specifies Python
scripts that should be installed as such. To install a script called `go_foo.py`
from your package, the call to `setup` would include the line:

    #!py
    scripts = ['go_foo.py'],

Just make sure you put the relative path to your script, not just its name
(e.g. `scripts = ['scripts/foo_scripts/go_foo.py']`). Also, your script should
begin with a "shebang" line with "python" in it, like:

    #!python
     #! /usr/bin/env python

`distutils` will automatically replace this line with the current interpreter
location during installation.

If your package is more complex than the simple one discussed here, take a look
at both the [`setuptools`](https://pythonhosted.org/setuptools/setuptools.html)
documentation and ["Distributing Python Modules"](http://docs.python.org/2/distutils/index.html) 
from the official documentation. Between the two, you should be able to
straighten out any issues you might have encountered.
