from setuptools import find_packages, setup

setup(
    name="datapipe_quickstart",
    packages=find_packages(),
    install_requires=["dagster", "dagster-cloud", "duckdb", "dagster-duckdb"],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
