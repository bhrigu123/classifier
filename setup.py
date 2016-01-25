
from setuptools import setup
from bin import name, version, description

setup(name=name,
      version=version,
      description=description,
      long_description=open('README.md').read(),
      url="http://github.com/bhrigu123/classifier",
      author="Bhrigu Srivastava",
      author_email="captain.bhrigu@gmail.com",
      license='MIT',
      packages=["classifier"],
      scripts=["bin/classifier"],
      zip_safe=False,
      platforms=['Linux', 'OSX'],
      classifiers=[
          'Intended Audience :: End Users/Desktop',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
      ],
)
