from setuptools import setup, find_packages

setup(
    name='django-secux',
    version='1.7.0',
    description='A lightweight Django security package with rate limiting decorator',
    author='XO Aria',
    author_email='hf18950@gmail.com',
    url='https://github.com/xo-aria/django-secux',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=2.2',
        'Pillow>=9.0.0',
    ],
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
