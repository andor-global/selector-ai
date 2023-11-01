# genl

Generate New Look

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)

## Overview

GENL is an essential part of your daily routine designed for creating your looks and style based on your personality.
We understand that fashion isn't just about what you wear, it is a reflection of who you are.
That's why we've created a platform you'll want to use every day, to simplify your style and shopping journey, and empower your individuality, all driven by cutting-edge AI technology.

## Project Structure

This project follows a specific directory structure:

- `/api`: API for interacting with model
  - `/db`: Contains db connection and models
  - `/routers`: API routers for handling requests
- `/machine_learning`: Contains machine learning code and notebooks
- `/tests`: Automated testing for the model.
- `requirements.txt`: Python package requirements

## Getting Started

### Setting up environment in Windows (WSL)

- NOTE: Some requirements are only available on Unix based OS. If you are on Windows. either use PyCharm, Docker or WSL.
- [How to install WSL](https://learn.microsoft.com/en-us/windows/wsl/install)

After installing WSL Ubuntu, update the package list, install pip and [virtualenv](https://pypi.org/project/virtualenv/).

```bash
$ sudo apt update
$ sudo apt-get install python3-pip
$ sudo pip install virtualenv
```

###

```bash
# after installing wsl start the virtual machine
$ wsl
$ git clone https://github.com/GENLapp/genl.git
$ cd genl
# create virtual environment for python
$ virtualenv venv
# enter the virtual environment
$ source ./venv/bin/activate
$ pip install -r requirements.txt
$ uvicorn api.main:app --reload
```

## Usage

### Run Dev Server

```bash
uvicorn api.main:app --reload
```

### Run Model

```bash
# command to only run the model
```

### Test the Model

```bash
# run automated tests for the model
```
