# Lemming

[![IBM](https://img.shields.io/badge/IBM%20Research-AI-red)](https://research.ibm.com)
[![Reagraph](https://img.shields.io/badge/REAGRAPH-green)](https://reagraph.dev)
[![AI](https://img.shields.io/badge/AI-ForbidIterative-purple)](https://github.com/IBM/forbiditerative)
[![AI](https://img.shields.io/badge/AI-Plan4Past-blue)](https://github.com/whitemech/Plan4Past)
[![AI](https://img.shields.io/badge/AI-NL2LTL-cyan)](https://github.com/IBM/nl2ltl)

<br/>
<img src="https://user-images.githubusercontent.com/4764242/250650534-868a817a-38b2-425b-aaa4-b30721ae3698.png" width="30%" height="auto" />

This repository hosts the source code for **Lemming: A Guided Disambiguation Tool for Plan Selection**.
Lemming makes use of landmarks to proactively guide the user to select a plan from a set of plans
while greedily minimizing the number of disambiguation points. It also provides multiple views into the set of
plans that need to be disambiguated, reflecting different considerations for the user in terms of how much
information they need to deal with during the disambiguation process.

> 🏆 The first Lemming appears in the ICAPS 2023 System Demonstration Track in Prague, where its integration with
> the [NL2LTL](https://github.com/IBM/nl2ltl) package was the runners-up for the People's Choice Best System Demonstration
> Award. Read more about it [here](https://icaps23.icaps-conference.org/demos/papers/692_paper.pdf).

## Setting up locally

[![Carbon](https://img.shields.io/badge/carbon-v11-black)](https://www.carbondesignsystem.com)
[![Python](https://img.shields.io/badge/python-3.10-dark%20green)](https://www.carbondesignsystem.com)

### Clone the repository and its submodules

```bash
user:~$ git clone git@github.com:IBM/lemming.git --recursive
user:~$ cd lemming
```

### Change to a virtual environment

We also strongly recommend using a virtual environment, such
as [anaconda](https://www.anaconda.com/), for development.

```bash
user:~$ conda create --name lemming python=3.10.11
user:~$ conda activate lemming
```

### Install Dependencies

```bash
(lemming) user:~$ pip install -e .
```

Set up NL2LTL integration without the Rasa dependency and build submodules.

```bash
(lemming) user:~$ pip install nl2ltl --no-deps
(lemming) user:~$ pip install pylogics openai==0.27.8 rasa==3.6.15
(lemming) user:~$ brew install autoconf automake libtool # for MacOS
(lemming) user:~$ ./scripts/build-submodules.sh
(lemming) user:~$ pip install --upgrade --no-deps --force-reinstall pydantic==2.5.2
```

In order to use the NL2LTL Integration, you must add your OpenAI API key 
to your environment variables with the name `OPENAI_API_KEY`.

### Start the Lemming Server

The Swagger page will show up at http://localhost:8000/docs. The OpenAPI spec can be obtained from the swagger page.

```bash
(lemming) user:~$ python -m uvicorn main:app --reload
```

### Start the Lemming Client

```bash
user:~$ yarn install
user:~$ yarn start
```

## Contributing

Contributions are welcome! 🤗 For instructions on setting up, go [here](docs/CONTRIBUTING.md).

## Citing our work

### ICAPS 2023 Demonstration

[`download`](https://icaps23.icaps-conference.org/demos/papers/692_paper.pdf)

```
@inproceedings{lemming,
title={{Lemming: A Guided Disambiguation Tool for Plan Selection}},
author={Jungkoo Kang and Tathagata Chakraborti and Michael Katz and Shirin Sohrabi and Francesco Fuggitti},
booktitle={ICAPS System Demonstration Track},
year={2023}}
```
