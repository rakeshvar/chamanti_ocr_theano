# -*- coding: utf-8 -*-

from setuptools import setup

requirements = open('requirements.txt').read().splitlines()

setup(
    name='chamanti_ocr',
    version='0.1',
    description='Telugu OCR framework using RNN, CTC in Theano & Python3',
    url='https://github.com/rakeshvar/chamanti_ocr',
    author='Rakeshvar Achanta',
    author_email='rakeshvar@gmail.com',
    license='Apache',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache License',
        'Programming Language :: Python :: 3',
    ],
    keywords='telugu ocr',
    install_requires=requirements,
    py_modules=['.py', 'rnn_ctc', 'lab', 'telugu'],
    package_data={
        '': ['*.ast']
    },
    include_package_data=True,
)
