import os

try:
    from setuptools import setup, find_packages
except ImportError, e:
    print "You need to install Python setuptools or distutils first!"
    exit(1)
    
dependecy = [] # list of dependencies That negar needs to install

# Here we check if PySide is not installed then install it with pypi ;-)
try:
    import PyQt4
except ImportError:
    #dependecy.append("PyQt4")
    print "Negar needs PyQt4 to run gui.\nI can install it for you over pypi but\
    it'll take too much time. Do you want to I do it for you?"
    answer = raw_input('(y/n):')
    if answer == 'n':
        exit(1)
    elif answer == 'y':
        pass
    
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
    
setup(
    name = "PyPomo",
    version = "0.5.0",
    author = "Shahin Azad",
    author_email = "ishahinism@gmail.com",
    include_package_data = True,
    packages = find_packages() + ['src'],
    package_dir={'src': 'src'},
    package_data={'src/graphics': ['graphics/*.svg'], 'src/sounds': ['sounds/*.wav']},
    description = "A pomodoro time management system software.",
    license = "GPL",
    keywords = "time time-management",
    url = "http://shahinism.github.com/pypomo",
    install_requires = dependecy,
    entry_points={
        'console_scripts': [
            'pypomo = src.PyPomo:main',
        ],
    },
    long_description=read
    ('README.txt'),    
)
