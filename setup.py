"""Setup configuration for AI Safety Library."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-safety-lib",
    version="0.2.0",
    author="Mukilan A.M",
    author_email="mukilanam06@gmail.com",
    description="A comprehensive library for AI safety monitoring, risk assessment, fairness, and explainability",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MUKILAN0608/ai_safety_lib",
    packages=find_packages(exclude=["tests", "examples", "docs"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords="ai safety monitoring drift detection fairness explainability risk-assessment mlops",
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "api": [
            "fastapi>=0.100.0",
            "uvicorn[standard]>=0.23.0",
            "pydantic>=2.0.0",
        ],
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0",
            "isort>=5.12",
            "flake8>=6.0",
            "mypy>=1.0",
            "bandit>=1.7",
            "safety>=2.3",
        ],
        "docs": [
            "sphinx>=5.0",
            "sphinx-rtd-theme>=1.2",
            "myst-parser>=1.0",
        ],
        "all": [
            "fastapi>=0.100.0",
            "uvicorn[standard]>=0.23.0",
            "pydantic>=2.0.0",
            "requests>=2.28.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-safety-server=api_server:run_server",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/MUKILAN0608/ai_safety_lib/issues",
        "Source": "https://github.com/MUKILAN0608/ai_safety_lib",
        "Documentation": "https://github.com/MUKILAN0608/ai_safety_lib#readme",
    },
)
