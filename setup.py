from pathlib import Path
from setuptools import setup


def read_version() -> str:
    version_file = Path(__file__).parent / "git_ok.py"
    for line in version_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("__version__"):
            return line.split("=", 1)[1].strip().strip('"\'')
    raise RuntimeError("Unable to find __version__ in git_ok.py")


ROOT = Path(__file__).parent
README = (ROOT / "README.md").read_text(encoding="utf-8")

setup(
    name="git-ok",
    version=read_version(),
    description="Check what's not backed up in your Git repository before you delete it.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Zhenye Dong",
    author_email="dongzhenye@gmail.com",
    url="https://github.com/dongzhenye/git-ok",
    project_urls={
        "Source": "https://github.com/dongzhenye/git-ok",
        "Issues": "https://github.com/dongzhenye/git-ok/issues",
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Version Control :: Git",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.8",
    py_modules=["git_ok"],
    entry_points={"console_scripts": ["git-ok=git_ok:main"]},
)
