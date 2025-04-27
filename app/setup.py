from setuptools import setup, find_packages

setup(
    name="nz-adventure",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask==3.0.2",
        "google-cloud-firestore==2.15.0",
        "google-cloud-storage==2.14.0",
        "python-dotenv==1.0.1",
        "gunicorn==21.2.0",
    ],
    extras_require={
        "dev": [
            "pytest==8.0.0",
            "pytest-cov==6.1.1",
            "black==24.1.1",
            "flake8==7.0.0",
            "isort==5.13.2",
            "mypy==1.8.0",
            "types-flask==1.1.6",
            "bandit==1.7.7",
            "safety==2.3.5",
        ],
    },
) 