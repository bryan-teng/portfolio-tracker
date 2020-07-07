import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyportfoliotracker", # Replace with your own username
    version="0.0.1",
    author="Bryan Teng",
    author_email="teng.weiyan.bryan@gmail.com",
    description="Track the performance of your portfolio of equities vs an index",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bryan-teng/portfolio-tracker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)