from distutils.core import setup

setup(name='TWStock',
	version='1.0',
	description='TWStock cores, including downloading data and data reader classes.',
	author='XTT',
	author_email='meteorologytoday@gmail.com',
	packages=['TWStock', 'TWStock.core', 'TWStock.helper', 'TWStock.scripts', 'TWStock.downloader'],
	package_dir = {'' : 'src'}
)
