from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A data scraper for Etsy stores'
LONG_DESCRIPTION = 'A data scraper for Etsy stores which allows you to collect product and store details using Beautiful Soup and Requests.'

CLASSIFIERS = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.7'
]
 
setup(
  name='EtsyScraperLib',
  version=VERSION,
  author='v0rkath',
  author_email='<x02@fastmail.com>',
  description=DESCRIPTION,
  long_description_content_type="text/markdown",
  long_description=LONG_DESCRIPTION,  
  packages=find_packages(),
  install_requires=['beautifulsoup4', 'requests'],
  keywords=['etsy', 'scraper', 'data', 'store', 'shop', 'price'], 
  license='MIT', 
  classifiers=CLASSIFIERS
)
