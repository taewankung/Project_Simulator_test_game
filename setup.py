import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
#README = open(os.path.join(here, 'README.md')).read()
#CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()


CONTROLLER = True
COMPUTE_NODE = True

requires = [
    'pygame',
    'Cython',
    'kivy'
]


scripts = []
setup(name='sim_map',
      version='0.0',
      description='',
 #     long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python :: 3",
      ],
      author='Phutthewan Yangyuenyong',
      author_email='taewankung@gmail.com',
      scripts=scripts,
      license='xxx License',
      packages=find_packages(),
      keywords='Runing naga project',
      #      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      #      tests_require=requires,
      #      test_suite="nokkhum-controller",
      )
