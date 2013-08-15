## PyPI

[PyPI, the Python Package Index](http://pypi.python.org/pypi) (formerly known as
"the Cheeseshop") is a central database of publicly available Python packages. 
PyPI is where your project's releases "live." One your package, and its
associate meta-data, has been uploaded to PyPI, others can download and install
it using `pip` or `easy_install`. This point bears repeating: even if your
project is available on GitHub, it's not until a release is uploaded to PyPI
that your project is useful. Sure, someone could clone your git repo and
manually install it directly, but *far* more people just want to `pip install`
it.

#### Initial upload

You'll be interacting with PyPI through `setuptools` and the `setup.py` script. 
If you've completed all of the steps in the previous sections, you're likely 
ready to bundle up your package, upload it to PyPI, and make it available to the
world!

If this is the first time this particular package is being uploaded to PyPI, you'll 
first need to *register* it:

    $ python setup.py register

*Note: if you don't yet have a free PyPI account, you'll need to make one now to be
able to register the package.* After you've followed `register` prompts, you're ready 
to create your distributable package and upload it to PyPI:

    $ python setup.py sdist upload

The command above builds a source distribution (`sdist`) and uploads it to PyPI. If your
package isn't pure Python (that is, you have binaries that need to be built), you'll 
need to do a binary distribution. See the `setuptools` documentation for more info.

#### Releases and version numbers

PyPI uses a *release version* model to decide which version (if you've uploaded
more than one) of your package should be available by default. After the initial
upload, you'll need to create a *release* with a new *version number* each time you
want your updated package to be made available on PyPI. Managing your 
version number can actually be a faily complex topic (I
would highly suggest *semmantic versioning*). I'll leave the *how* up to you, but 
the `version` used in `setup.py` **must** be "higher" than what's currently 
on PyPI for PyPI to consider the package a new version.

##### Workflow

After uploading your first release to PyPI, the basic workflow is this: 

1. Do some work on your package (i.e. fix bugs, add features, etc)
1. Make sure the tests pass
1. "Freeze" your code by creating a `release` branch in git-flow
1. Update the `__version__` number in your package's `__init__.py` file
1. Run `python setup.py sdist upload` to upload the new version of your package to PyPI

Users depend on you to release frequently enough to get bug fixes out. As long
as you're properly managing your version numbers, there is no such thing as
releasing "too frequently." Remember: your users aren't manually maintaining the 
different versions of every Python package they have installed.
