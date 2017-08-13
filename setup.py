from setuptools import setup

setup(
    name='ansibly',
    version='0.1',
    py_modules=['ansibly'],
    install_requires=[
        'Click',
        'sh'
    ],
    entry_points='''
        [console_scripts]
        ansibly=ansibly:cli
    ''',
)