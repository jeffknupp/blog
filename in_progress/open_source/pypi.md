## PyPI

[PyPI, the Python Package Index](http://pypi.python.org/pypi) (formerly known as
"the Cheeseshop") is a central database of publicly available Python packages. 
PyPI is where your users will find your project. It's also the package
repository that tools like `pip` search when someone tries to `pip install` your
project. 

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
