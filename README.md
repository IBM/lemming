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


## Run Docker Images

Build a front-end image.

```
user:~$ yarn install
user:~$ yarn build
<!-- user:~$ docker build --progress plain -t lemming-front -f Dockerfile_frontend . -->
```

To build a Backend image, pip can be configured with `pip.conf` at the project root. This is to go around sporadic python index server issues. Your OpenAI API Key (`OPENAI_API_KEY`) should be defined in `docker-compose.yml` to use `NL2LTL` service at the backend

<!-- Build a backend image. Make sure that there is no local cache for cmake or make for symk.

```
user:~$ docker build --progress plain -t lemming-backend -f Dockerfile_backend .
``` -->
To bring up Lemming service,

```
docker-compose -f docker-compose.yml up
```

To teardown Lemming service,

```
docker-compose -f docker-compose.yml down
```


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

### Install Lemming Dependencies

```bash
(lemming) user:~$ pip install -e .
```

### Use the NL2LTL integration (optional)

First, install `nl2ltl` and `plan4past` with:

```bash
(lemming) user:~$ pip install -e ".[nl2ltl]"
```

Then, build the `symk` planner with:

```bash
(lemming) user:~$ ./scripts/build-submodules.sh
```

(Make sure you have `autoconf`, `automake`, `cmake`, `g++`, `libtool`, and
`make` pre-installed on your system).

In order to use the NL2LTL Integration, don't forget to add your OpenAI API key
to your environment variables with the name `OPENAI_API_KEY`.

```bash
(lemming) user:~$ export OPENAI_API_KEY=<your_openai_api_key>
```

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

You can install dev dependencies with:

```bash
(lemming) user:~$ pip install -e ".[dev]"
```

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
