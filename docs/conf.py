# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'DearDoc'
copyright = '2023, kakako'
author = 'kakako'

version = 'dev'
release = 'dev'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # 'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'autoapi.extension',
]

# -- Autoapi configuration ---------------------------------------------------
# https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html
autoapi_type = 'python'
autoapi_dirs = [
	'../editor',
	'../engine',
	# '../extensions',
	'../launcher',
	'../tools',
]
autoapi_options = [
	'members',
	'undoc-members',
	# 'private-members',
	# 'special-members',
	# 'show-module-summary',
	'show-inheritance',
]
autoapi_ignore = [
	'*pyqtads*',
]
autoapi_python_class_content = 'both'

# def skip(app, what, name, obj, skip, options):
# 	if name.endswith('__init__') and obj.docstring:
# 		return False
# 	return skip

# def setup(sphinx):
# 	sphinx.connect('autoapi-skip-member', skip)


templates_path = ['_templates']
exclude_patterns = ['_build', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
# html_title = 'Welcome to DearDoc!'
html_favicon = 'favicon.ico'
html_show_sourcelink = False

# -- Options for ReadTheDocs theme -------------------------------------------------
# https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
html_theme_options = {
    'titles_only'         : True,
    'display_version'     : True,
    'sticky_navigation'   : True,
    'collapse_navigation' : False,
    'style_external_links': False,
    'navigation_depth'    : -1,
}

