"""Compatibility installer for Python environments with older build tooling."""

from setuptools import find_packages, setup


setup(
    name="average-slope-pk",
    version="0.1.0",
    description="Average slope from concentration-time data through observed Tmax",
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.9",
    entry_points={"console_scripts": ["average-slope=average_slope.cli:main"]},
)
