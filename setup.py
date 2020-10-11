from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='pwmled',
    version='1.5.2',
    description='Control LEDs connected to a micro controller using pwm.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/soldag/python-pwmled/',
    license='MIT',
    author='soldag',
    author_email='soren.oldag@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pigpio==1.35',
        'adafruit-blinka==5.5.1',
        'adafruit-circuitpython-pca9685==3.3.2',
        'python-singleton==0.1.2',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ]
)
