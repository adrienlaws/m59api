from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="m59api",
    version="0.1.31",
    author="Adrien Laws",
    author_email="laws.adrien@gmail.com",
    description="A FastAPI-based API for managing the Meridian 59 server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adrienlaws/m59api",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "fastapi>=0.70.0",
        "uvicorn>=0.15.0",
        "httpx>=0.23.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: FastAPI",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "m59api=m59api.cli:main",
        ],
    },
    include_package_data=True,  # Include additional files specified in MANIFEST.in
)
