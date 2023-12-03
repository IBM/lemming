# Contributing to Lemming

Adding new features, improving documentation, fixing bugs, or writing tutorials are all examples of helpful contributions. 
Furthermore, if you are building on the research work, we strongly encourage you to read our whitepapers [here](https://github.com/IBM/lemming#citing-our-work).

Bug fixes can be initiated through GitHub pull requests or PRs. 
When making code contributions to Lemming, we ask that you follow the `PEP 8` coding standard 
and that you provide unit tests for the new features.

This project uses [DCO](https://developercertificate.org/). 
You must sign off your commits using the `-s` flag in the commit message.

### Example commit message

```bash
git commit -s -m 'informative commit message'
```

## Setting up the dev environment

![BLACK](https://img.shields.io/badge/code%20style-black-black)
![PRETTIER](https://img.shields.io/badge/code%20style-prettier-black)
![PYLINT](https://img.shields.io/badge/linting-pylint-yellow)
![FLAKE8](https://img.shields.io/badge/linting-flake8-yellow)
![MYPY](https://img.shields.io/badge/typing-mypy-orange)


First, follow the general setup instructions [here](../README.md). Then install the dev-specific dependencies and pre-commit hooks.

```bash
(lemming) user:~$ pip install -e '.[dev]'
(lemming) user:~$ pre-commit install
```

Whether you are contributing a new interaction pattern or addressing an existing issue, you need to ensure that the unit tests pass. 
The existing tests are housed [here](../server/tests).

Once all the tests have passed, and you are satisfied with your contribution, open a pull request into the `main` branch 
from **your fork of the repository** to request adding your contributions to the main code base.
