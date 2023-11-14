from setuptools import find_packages, setup

package_name = "bezier_lib"

with open(f"./{package_name}/README.md", "r") as f:
    long_description = f.read()

setup(
    name=package_name,
    packages=find_packages(include=[package_name]),
    version="0.0.1",
    description="Bezier functions for calculating bezier points and angles",
    long_description=long_description,
    url="google.com",
    long_description_content_type="text/markdown",
    author="g00z-g00z",
    license="MIT",
    install_requires=["numpy", "bezier", "sympy"],
    test_requires=["pytest"],
    extras_require={"dev": ["pytest", "twine"]},
    setup_requires=["pytest-runner"],
    test_suite="awesome_lib/tests",
    python_requires=">=3.9",
)
