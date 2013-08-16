# ReadTheDocs for Continuous Documentation Integration

While PyPI has an official documentation site ([pythonhosted.org](http://www.pythonhosted.org)), 
[ReadTheDocs](https://readthedocs.org/) provides a better experience. Why?
ReadTheDocs has great integration with GitHub. Once you register on
ReadTheDocs, you'll see all of your GitHub repos. Select the appropriate repo,
do some minor configuration, and you're documentation will be automatically
regenerated after each commit to GitHub.

Configuring your project should be a straightforward affair. There are a few
things to remember, though. Here's a list of configuration fields and the
values you should use which might not be immediately obvious:

* Repo: https://github.com/<github_username>/<project_name>.git
* Default Branch: `develop`
* Default Version: `latest`
* Python configuration file: (leave blank)
* Use `virtualenv`: (checked)
* Requirements file: `requirements.txt`
* Documentation Type: Sphinx HTML
