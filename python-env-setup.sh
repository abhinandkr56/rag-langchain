ENV_NAME=langchain-dev
PYTHON_VERSION=3.12

# Setting up the environment using pipenv

python3.12 -m pip install pipenv

pipenv install ipykernel langchain python-dotenv unstructured \
	pgvector langchain-openai tiktoken psycopg2-binary \
	langchain-text-splitters markdown

pipenv shell

# to remove the environment
pipenv clean


# Setting up the environment using conda
# conda create --name ${ENV_NAME} python=${PYTHON_VERSION}

# ENV_LOCATION=$(conda env list | grep $ENV_NAME | awk '{print $2}')

# Add the suffix to the location
# PIP_LOCATION=$ENV_LOCATION/bin/pip

# Assign the alias
# alias pip=$PIP_LOCATION

# conda activate ${ENV_NAME}

# conda env list

# python -m ipykernel install --user --name "${ENV_NAME}-kernel" --display-name "Python (${ENV_NAME})"

# to remove the environment
# conda remove -n ${ENV_NAME} --all -y