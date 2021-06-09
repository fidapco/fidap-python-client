from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='fidap',
    version='0.0.15',
    description='Access clean external data easily.',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Ashish Singal',
    author_email='ashish.singal1@gmail.com',
    keywords=['API', 'data', 'financial', 'economic', 'fidap'],
    url='https://github.com/fidapco/fidap-python',
    download_url='https://pypi.org/project/fidap/',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)

install_requires = [
    'pandas >= 0.14',
    'numpy >= 1.8',
    'requests >= 2.7.0',
    'python-dotenv >= 0.15.0',
    'delta-sharing'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
