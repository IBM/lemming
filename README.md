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
Read more about it [here](https://icaps23.icaps-conference.org/demos/papers/692_paper.pdf).

## Setting up locally

### Server

0. Clone the repository and its submodules

```bash
user:~$ git clone git@github.com:IBM/lemming.git --recursive
```

1. Change a virtual environment to the one for `Lemming`.

```bash
user:~$ cd server/
user:~$ pip install -e .
```

2.  For the NL2LTL integration, install it without the Rasa dependency and
    build submodules.

```bash
user:~$ pip install nl2ltl --no-deps
user:~$ pip install pylogics openai==0.27.8
user:~$ ./scripts/build_submodules.sh
```

3. Start a server. The Swagger page is shown at http://localhost:8000/docs. The OpenAPI spec can be obtained from the swagger page.

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
