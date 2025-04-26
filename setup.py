from setuptools import setup, find_packages

setup(
    name="reactagent",
    version="1.0.0",
    description="Implementation of ReAct framework",
    author="Tatevik Abrahamyan",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pymongo",
        "gym",
        "requests",
        "protobuf",
        "beautifulsoup4",
        "google-genai"
    ],
    python_requires=">=3.8",
)
