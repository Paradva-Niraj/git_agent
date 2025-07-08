from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

setup(
    name='git-agent',
    version='1.0.3',
    packages=find_packages(),
   install_requires=[
    "python-dotenv",
    "google-generativeai"
    ],
    entry_points={
    "console_scripts": [
         "git-agent=git_agent.git_agent:main"
    ]
    },
    long_description = description,
    long_description_content_type="text/markdown",
)