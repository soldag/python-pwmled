from setuptools import setup, find_packages

setup(
    name='pwmled',
    version='1.5.1',
    description='Control LEDs connected to a micro controller using pwm.',
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
