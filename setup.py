from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flusso",
    version="0.1.0",
    author="Tomiwa Adey",
    author_email="tomiwa@tomiwaadey.com",
    description="Rust Inspired Type-Safe Errors and Missing Values for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gum-tech/flusso",
    packages= find_packages(),
    license="MIT",
    keywords=['python', 'monad', 'rust', 'functional-programming', 'option', 'result'],
    extras_require={
        "dev": ["pytest>=7.0", "pytest-asyncio", "twine>=4.0.2"], #pip install -e .[dev]
    },
    python_requires=">=3.7",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
