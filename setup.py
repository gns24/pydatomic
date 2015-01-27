try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name="pydatomic",
      version="0.1.0",
      author="Graham Stratton",
      author_email="gns24@beasts.org",
      description="Datomic REST API client",
      long_description=open('README.rst').read(),
      url="https://github.com/gns24/pydatomic",
      install_requires=['requests'],
      license='mit',
      packages=['pydatomic'],
      classifiers=['Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Topic :: Software Development',
            'Programming Language :: Python',
            'Operating System :: OS Independent']
    )
