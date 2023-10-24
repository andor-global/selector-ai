# genL

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
  - `routers`: API routers for handling requests
- `/machine_learning`: Contains machine learning code and notebooks
- `/tests`: Automated testing for the model.
- `requirements.txt`: Python package requirements

## Getting Started

```bash
git clone https://github.com/GENLapp/genL.git
cd genL
pip install -r requirements.txt
```

## Usage

### Run Dev Server

```bash
uvicorn api.main:app --reload
# server started at http://127.0.0.1:8000/
```

### Run Model

```bash
# command to only run the model
```

### Run Docker

```bash
# commands to run docker
```

### Test the Model

```bash
# run automated tests for the model
```
