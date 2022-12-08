from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
  'sentence_transformers',
    'numpy',
    'httpx',
'requests'
]

setup(
    name="text2music",
    version="0.1.0",
    author="NLP Guild",
    author_email="tao.xiang@tum.de",
    description="A package for text-to-music generation",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/NLP-Guild/text2music",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
  "Programming Language :: Python :: 3.8",
  "License :: OSI Approved :: MIT License",
    ],
)