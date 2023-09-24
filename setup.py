from setuptools import setup

with open("Readme.md", "r") as f:
    long_description = f.read()

VERSION = '0.3'
DESCRIPTION = 'Box Office Mojo Information'
# Setting up
setup(
    name="boxoffice_api",
    version=VERSION,
    author="Pourya Mohamadi",
    author_email="fresh.pourya@gmail.com",
    description="Unofficial Python API for Box Office Mojo",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/Stink-Po/boxoffice_api",
    packages=["boxoffice_api"],
    install_requires=['requests', 'bs4'],
    keywords=['python', 'movie', 'movies', 'boxoffice_api', 'box office', 'scraping'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
    ]
)
