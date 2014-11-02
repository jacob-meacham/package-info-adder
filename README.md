package-info-adder
==================

Adds package-info.java files to an existing Java project.

usage: package-info-adder.py [-h] [-f] [-r] [-v] [-t TEMPLATE]
                             directory parent_package

positional arguments:
  directory
  parent_package

optional arguments:
  -h, --help            show this help message and exit
  -f, --force           Overwrite existing
  -r, --recursive       Make crawl recursive
  -v, --verbose
  -t TEMPLATE, --template TEMPLATE
                        optional template file. use __PACKAGE__ for package
                        delcaration