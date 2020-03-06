from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mkdocs-table-reader-plugin',
    version='0.1.0',
    description='MkDocs plugin to directly insert tables from files into markdown.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='mkdocs plugin',
    url='https://github.com/timvink/mkdocs-table-reader-plugin',
    author='Tim Vink',
    author_email='vinktim@gmail.com',
    license='MIT',
    python_requires='>=3.5',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'mkdocs>=1.0',
        'pandas>=1.0',
        'tabulate>=0.8.6'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'table-reader = mkdocs_table_reader_plugin.plugin:TableReaderPlugin'
        ]
    }
)
