import argparse
import os
import re
from functools import partial

DEFAULT_TEMPLATE = """package __PACKAGE__;

"""

def write_package_info(directory, parent_package, template, verbose):
    full_name = directory.replace('\\', '.').replace('/', '.').rstrip('.')
    parent_idx = full_name.find(parent_package)
    if parent_idx == -1:
        print 'Could not find the parent package {0} in the directory {1}'.format(parent_package, directory)
        return

    package_name = full_name[parent_idx:]
    if verbose:
        print 'writing package-info.java to {0} as package {1}'.format(directory, package_name)
    content = template.replace('__PACKAGE__', package_name)
    with open(os.path.join(directory, 'package-info.java'), 'w+') as f:
        f.write(content)

def test_directory(dirname, files, parent_package, template, args):
    force, verbose = args.force, args.verbose
    java_regex = re.compile('\.java$', re.IGNORECASE)
    package_info_regex = re.compile('^package-info\.java$', re.IGNORECASE)

    # A tiny bit of pointless functional exercising here...
    def exists(regex, before, to_search):
        return before or regex.search(to_search) != None

    java_file_exists = reduce(partial(exists, java_regex), files, False)
    package_info_exists = reduce(partial(exists, package_info_regex), files, False)

    if java_file_exists:
        if not package_info_exists or force:
            write_package_info(dirname, parent_package, template, verbose)
        elif verbose:
            print 'java source found at {0}, but a package-info.java file already exists'.format(dirname)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--force', action='store_true', help='Overwrite existing')
    parser.add_argument('-r', '--recursive', action='store_true', help='Make crawl recursive')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-t', '--template', help='optional template file. use __PACKAGE__ for package delcaration')
    parser.add_argument('directory')
    parser.add_argument('parent_package')
    args = parser.parse_args()

    template = DEFAULT_TEMPLATE
    if args.template != None:
        with open(args.template, 'r') as f:
            template = f.read()
    
    if not args.recursive:
        test_directory(args.directory, os.listdir(args.directory), args.parent_package, template, args)
    else:
        for dirname, _, files in os.walk(args.directory):
            test_directory(dirname, files, args.parent_package, template, args)
