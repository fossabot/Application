from setuptools import setup
setup(
    name='PedalPi - Application',
    packages=['application', 'test'],
    test_suite='test',
    install_requires=['PedalPi-PluginsManager'],
    dependency_links=['https://github.com/PedalPi/PluginsManager/tarball/master#egg=PedalPi-PluginsManager']
)
