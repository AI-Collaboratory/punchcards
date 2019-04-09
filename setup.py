from setuptools import setup, find_packages

setup(name="punchcards",
      version='0.1',
      description='Punch Card Reader',
      url='http://github.com/UMD-DCIC/punchcards',
      author='Gregory N. Jansen',
      author_email='jansen@umd.edu',
      license='GPL 3.0',
      packages=['punchcards'],
      install_requires=['docopt','Pillow','numpy'],
      zip_safe=False)
