# Lemming

[![Carbon](https://img.shields.io/badge/carbon-v11-blue)](https://www.carbondesignsystem.com)
[![Carbon](https://img.shields.io/badge/python-3.10-green)](https://www.carbondesignsystem.com)

<br/>
<img src="https://user-images.githubusercontent.com/4764242/250650534-868a817a-38b2-425b-aaa4-b30721ae3698.png" width="30%" height="auto" />

This repository hosts the source code for **Lemming: A Guided Disambiguation Tool for Plan Selection**.
Lemming makes use of landmarks to proactively guide the user to select a plan from a set of plans
while greedily minimizing for the number of disambiguation points. It also provides multiple views into the set of
plans that need to be disambiguated, reflecting different considerations for the user in terms of how much
information they need to deal with during the disambgiuation process.

The first Lemming appears in the ICAPS 2023 System Demonstration Track in Prague.
Read more about it [here]().

## Setting up locally

### Server

1. Clone `watson-ai-planning` repo at an arbitrary folder

```bash
user:~$ git clone git@github.ibm.com:ai-foundation/watson_ai_planning.git
```

1. Make sure that a local virtual environment for `watson-ai-planning` is activate.

2. Checkout "DataModel" branch.

```bash
cd watson_ai_planning
user:~$ git checkout DataModelPlansToGraph
```

3. Install dependencies with `pip` command at the folder containing `pyproject.toml`.

```bash
user:~$ pip install -e .
```

4. Upgrade `build`.

```bash
user:~$ python -m pip install --upgrade build
```

5. Build a package (This step takes a while). The built artifacts will be located at `dist` folder.

```bash
user:~$ python -m build
```

6. Change a virtual environment to the one for `Lemming`.

7. Download watson-core version `1.25.0rc3` from [here](https://na.artifactory.swg-devops.com/ui/packages/pypi:%2F%2Fwatson-core/1.25.0rc3?name=watson-core&type=packages).

8. Install the downloaded python package.

```
user:~$ pip install <PATH_TO_DOWNLOADED_FILE>
```

9. Install the built `watson-ai-planning` package.

```bash
user:~$ pip install <PATH_TO_WHL_FILE>
```

For example, the command can look like this.

```bash
user:~$ pip install /Users/aiplanningmachine/Documents/projects/watson_ai_planning/dist/watson_ai_planning-0.1.dev210+ge39b9b1.d20230524-py3-none-any.whl
```

10. Move to the folder containing `Lemming` to install more dependencies.

```bash
user:~$ cd server/
user:~$ pip install -e .
```

11. Start a server. The Swagger page is shown at http://localhost:8000/docs. The OpenAPI spec can be obtained from the swagger page.

```bash
user:~$ python -m uvicorn main:app --reload
```

### Client

```bash
user:~$ yarn
user:~$ yarn start
```

## Citing our work

[`paper`](https://icaps23.icaps-conference.org/demos/papers/692_paper.pdf)

```
@inproceedings{lemming,
title={{Lemming: A Guided Disambiguation Tool for Plan Selection}},
author={Jungkoo Kang and Tathagata Chakraborti and Michael Katz and Shirin Sohrabi and Francesco Fuggitti},
booktitle={ICAPS System Demonstration Track},
year={2023}}
```
