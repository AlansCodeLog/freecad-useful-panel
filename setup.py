from setuptools import setup
import os
from freecad.useful_panel.version import __version__

version_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "freecad", "useful_panel", "version.py")

with open(version_path) as fp:
    exec(fp.read())

setup(name='freecad.useful_panel',
    version=str(__version__),
    packages=['freecad',
            'freecad.useful_panel'],
    maintainer="alan",
    maintainer_email="alanscodelog@gmail.com",
    url="https://github.com/alanscodelog/freecad-useful-panel",
    description="Freecad addon panel with some useful measuring and batch search/replace/export tools.",
    install_requires=[],
    include_package_data=True
)
