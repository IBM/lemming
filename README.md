# Lemming

[![Carbon](https://img.shields.io/badge/carbon-v11-blue)](https://www.carbondesignsystem.com)
[![Carbon](https://img.shields.io/badge/python-3.10-green)](https://www.carbondesignsystem.com)

<br/>
<img src="https://media.github.ibm.com/user/93001/files/c843e2f5-b515-4c1a-bcb2-988ca0bf40e7" width="40%" height="auto"/>

This repository hosts the source code for **Lemming: A Guided Disambiguation Tool for Plan Selection**.
Lemming makes use of landmarks to proactively guide the user to select a plan from a set of plans
while greedily minimizing for the number of disambiguation points. It also provides multiple views into the set of
plans that need to be disambiguated, reflecting different considerations for the user in terms of how much
information they need to deal with during the disambgiuation process.

The first Lemming appears in the ICAPS 2023 System Demonstration Track in Prague.
Read more about it [here]().

## Setting up locally

### Server

```bash
user:~$ cd server/
user:~$ pip install -r requirements.txt
user:~$ python server.py
```

### Client

```bash
user:~$ yarn
user:~$ yarn start
```

## Citing our work

```
@inproceedings{lemming,
title={{Lemming: A Guided Disambiguation Tool for Plan Selection}},
author={Michael Katz and Jungkoo Kang and Tathagata Chakraborti and Shirin Sohrabi},
booktitle={ICAPS System Demonstration Track},
year={2023}}
```
