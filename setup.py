import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="query-filter-builder",
    version="0.0.6",
    author="jmezo",
    author_email="jmezo@dataedge.hu",
    description="Generates sql filters with params from custom filter object.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://gitlab.dataedge/packages/query-filter-builder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
