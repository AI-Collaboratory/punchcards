from setuptools import setup, find_packages

setup(name="punchcards",
      version='0.1',
      description='Punch Card Reader',
      url='http://github.com/UMD-DCIC/punchcards',
      author='Gregory N. Jansen',
      author_email='jansen@umd.edu',
      download_url = 'https://github.com/UMD-DCIC/punchcards/archive/v_01.tar.gz',
      keywords = ['PUNCH', 'CARD', 'PUNCHCARD', 'IMAGE'],
      license='GPL 3.0',
      packages=['punchcards'],
      install_requires=['docopt','Pillow','numpy'],
      classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ],
      zip_safe=False)
