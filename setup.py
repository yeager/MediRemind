"""Setup script for MediRemind."""

from setuptools import setup, find_packages

setup(
    name="mediremind",
    version="0.1.0",
    description="Medicinpåminnare med bilder, ljud och bekräftelse",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="MediRemind Team",
    license="GPL-3.0",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "gui_scripts": [
            "mediremind = mediremind.__main__:main",
        ],
    },
    package_data={
        "mediremind": [
            "../data/**/*",
            "../po/*.po",
            "../po/*.pot",
        ],
    },
    data_files=[
        ("share/applications", ["data/se.mediremind.app.desktop"]),
    ],
    install_requires=[
        "PyGObject>=3.42",
        "pycairo>=1.20",
    ],
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: Swedish",
        "Programming Language :: Python :: 3",
        "Topic :: Desktop Environment",
        "Topic :: Utilities",
    ],
)
