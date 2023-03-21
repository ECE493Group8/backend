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

### Define model path

The backend expects a path to a trained Word2Med model, which it will query and use to form responses. See the [model](https://github.com/ECE493Group8/model) repository for more info on training a Word2Med model.

The model path is defined within a `.env` file in this directory. An example of such a `.env` file could be:

```sh
WORD2MED_MODEL_PATH=/path/to/word2medmodel.model
```

### Running Backend

```bash
make run
```

### Generating Documentation

```bash
make docs
```
