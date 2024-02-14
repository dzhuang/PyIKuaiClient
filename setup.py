from setuptools import find_packages, setup

from src import pyikuai


install_requires = [
    'requests',
]

setup(
    name='pyikuai',
    version=pyikuai.__version__,
    description="A Python client for interacting with IKuai routers",
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    classifiers=[
        # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='iKuai Router client API',
    author='Dong Zhuang',
    author_email='dzhuang.scut@gmail.com',
    url='https://github.com/dzhuang/PyIKuaiClient/',
    license='MIT',
    packages=find_packages("src"),
    include_package_data=True,
    zip_safe=True,
    install_requires=install_requires,
    package_dir={"": "src"},
    python_requires='>=3.6',
)
