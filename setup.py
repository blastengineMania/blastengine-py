import setuptools

setuptools.setup(
    name="blastengine",
    version="0.0.3",
    author="goofmint",
    author_email="atsushi@moongift.jp",
    description="blastengine is SDK for blastengine",
    long_description="blastengine is SDK for blastengine. It supports text and html email with attachments.",
    long_description_content_type="text/markdown",
    url="https://blastengine.jp/",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
