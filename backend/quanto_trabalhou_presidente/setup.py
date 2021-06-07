# -*- encoding: utf-8 -*-
# Source: https://packaging.python.org/guides/distributing-packages-using-setuptools/

import io
import re

from setuptools import find_packages, setup

dev_requirements = [
    'pylama==7.7.1',
    'pytest==6.2.4',
]
unit_test_requirements = [
    'pytest==6.2.4',
    'pytest-cov==2.12.1 '
]
integration_test_requirements = [
    'pytest==6.2.4 ',
    'pytest-cov==2.12.1'
]
run_requirements = [
    'fastapi>=0.65.1',
    'loguru>=0.5.3',
    'beautifulsoup4>=4.9.3',
    'requests>=2.25.1',
    'uvicorn>=0.14.0',
    'gunicorn>=20.1.0'
]

with io.open('./quanto_trabalhou_presidente/__init__.py', encoding='utf8') as version_f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()

setup(
    name="qtp",
    version=version,
    author="Rodrigo Guimarães Araújo",
    author_email="rodrigoara27@gmail.com.br",
    packages=find_packages(exclude='tests'),
    include_package_data=True,
    url="https://github.com/ratopythonista/quanto-trabalhou-presidente",
    license="COPYRIGHT",
    description="Quanto trabalhou o Presidente?",
    long_description=long_description,
    zip_safe=False,
    install_requires=run_requirements,
    extras_require={
         'dev': dev_requirements,
         'unit': unit_test_requirements,
         'integration': integration_test_requirements,
    },
    python_requires='>=3.8',
    classifiers=[
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.9'
    ],
)