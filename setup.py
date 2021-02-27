import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discordify",
    version="0.0.1",
    author="Arumugam Ramaswamy",
    author_email="rm.arumugam.2000@gmail.com",
    description="Convert your python code to a discord bot in less than 5 mintutes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arumugam666/discordify",
    scripts=["scripts/create_config.py", "scripts/run_discordify_app.py"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=["discordify"],
    python_requires=">=3.6",
)
