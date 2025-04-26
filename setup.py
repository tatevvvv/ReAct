from setuptools import find_packages, setup

setup(
    name="reactagent",
    version="1.0.0",
    description="Implementation of ReAct framework",
    author="Tatevik Abrahamyan",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9",          # ← bump from 3.8 → 3.9
    install_requires=[
        "pymongo",
        "gym",
        "requests",
        "protobuf",
        "beautifulsoup4",
        "google-genai>=1.0.0"         # ← correct package name
    ],
)
