from setuptools import setup, find_packages

setup(
    name="regex_project",
    version="0.1",
    description="A tool for validating and tokenizing regular expressions.",
    author="Kim Takala",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
