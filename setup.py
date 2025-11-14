from setuptools import setup, find_packages

setup(
    name="phishing-detector",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive phishing detection system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/phishing-detector",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Flask==2.3.2",
        "requests==2.31.0",
        "beautifulsoup4==4.12.2",
        "scikit-learn==1.3.0",
        "gunicorn==21.2.0",
        "gevent==23.9.1",
        "psutil==5.9.5",
    ],
    entry_points={
        "console_scripts": [
            "phishing-detector=main:main",
            "phishing-cli=cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)