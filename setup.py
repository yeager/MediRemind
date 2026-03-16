from setuptools import setup, find_packages

setup(
    name="mediremind",
    version="0.1.0",
    description="Simple medication reminder with GTK4/Adwaita",
    author="MediRemind",
    license="GPL-3.0",
    packages=find_packages(),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "mediremind=mediremind.__main__:main",
        ],
    },
    data_files=[
        ("share/applications", ["data/se.mediremind.app.desktop"]),
    ],
)
