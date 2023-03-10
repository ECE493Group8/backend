# word2med-backend

## Usage

API documentation can be found [here](https://ece493group8.github.io/word2med-backend/)

## Development Configuration

Follow these steps to run the word2med backend locally

### Setup

Clone this repository and initialize a virtual environment in the root directory using the tool of your choice. (e.g. [virtualenv](https://virtualenv.pypa.io/en/latest/))

```bash
git clone https://github.com/ECE493Group8/word2med-backend.git
cd word2med-backend
virtualenv venv
```

Activate your virtual environment

```bash
. venv/bin/activate
```

Install dependencies from requirements.txt

```bash
pip install -r requirements.txt
```

### Running Backend

```bash
make run
```

### Generating Documentation

```bash
make docs
```
