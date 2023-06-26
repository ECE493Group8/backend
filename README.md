# word2med-backend

## Usage

API documentation can be found [here](https://ece493group8.github.io/word2med-backend/)

### Postman

A [postman](https://www.postman.com/) collection with usage examples for each endpoint is exported to [`Word2Med.postman_collection.json`](./Word2Med.postman_collection.json).

To use, simply import this file within [postman](https://www.postman.com/).

## Development Configuration

Follow these steps to run the word2med backend locally

### Setup

Clone this repository and initialize a virtual environment in the root directory using the tool of your choice. (e.g. [virtualenv](https://virtualenv.pypa.io/en/latest/)). **Note that the virtual environment must use version python3.10 or greater.**

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

**Note:** If you have issues in this step, ensure you have the latest pip version by running the following with you venv activated:

```
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
```

### Define model path

The backend expects a path to a trained Word2Med model, which it will query and use to form responses. See the [model](https://github.com/ECE493Group8/model) repository for more info on training a Word2Med model.

The model path is defined in the `models.json` file. An example of such a file
could be:

```json
{
  "model_1": "path/to/my.model",
  "model_2": "another/path/to/my/other.model"
}
```

The key is the ID of the model. This must match the key of the model ID in the
frontend's `src/constants/models.js` file. The value is the path to the model
file.

### Running Backend

```bash
make run
```

### Generating Documentation

```bash
make docs
```
