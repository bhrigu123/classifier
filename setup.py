
from setuptools import setup

setup(name="classifier",
      version="1.5.1",
      description="Classify the files in your Downloads folder into suitable destinations.",
      url="http://github.com/bhrigu123/classifier",
      author="Bhrigu Srivastava",
      author_email="captain.bhrigu@gmail.com",
      license='MIT',
      package_dir={'classifier': 'src'},
      packages=['classifier'],
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'classifier=classifier:main',
          ],
      },
)
