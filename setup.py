from setuptools import setup

setup(
        name="classifier",
        version="1.6.5",
        description="Classify the files in your Downloads folder into suitable destinations.",
        url="http://github.com/bhrigu123/classifier",
        author="Bhrigu Srivastava",
        author_email="captain.bhrigu@gmail.com",
        license='MIT',
        packages=["classifier"],
        entry_points="""
             [console_scripts]
             classifier = classifier.classifier:main
        """,
        install_requires=[
            'arrow',
            'six>=1.10.0',
        ],
        zip_safe=False
)
