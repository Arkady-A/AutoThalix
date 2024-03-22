import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requirements = f.readlines()

install_requires = [req.strip() for req in requirements]

setuptools.setup(
    name="AutoThaliX",
    version="0.3.1",
    author="ArkadyA",
    author_email="arkadymirz@gmail.com",
    description="A set of tools to work with tales potentiostats. Uses tales_remote",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Arkady-A/autothalix",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=install_requires,
)
