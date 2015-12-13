
from setuptools import setup

setup(name="classifier",
	version="1.2",
	description="Classify the files in your Downloads folder into suitable destinations.",
	url="http://github.com/bhrigu123/classifier",
	author="Bhrigu Srivastava",
	author_email="captain.bhrigu@gmail.com",
	license='MIT',
	packages=["classifier"],
	scripts=["bin/classifier"],
	zip_safe=False)
