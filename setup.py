from setuptools import setup, find_packages

setup(
    name='pwmled',
    version='1.0.0',
    description='Control pwm leds on a Raspberry Pi.',
    url='https://github.com/soldag/python-pwmled/',
    license='MIT',
    author='soldag',
    author_email='soren.oldag@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pigpio',
        'adafruit-pca9685'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ]
)
