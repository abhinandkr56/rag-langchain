# Introduction 
Playpen for rag walkthrough using langchain and pgvector

# Getting Started
Change the permissions mode of shell scripts to execute using following command in the root folder
```sh
chmod +x *.sh
```

### Setup database
Run below command to pull the docker image and create a postgres container with necessary users along with enabling pgvector extension. See the script for more details, in a nutshell it will create another file called `init-user-db.sh` and run it inside the container, post that exec to the container
```sh
./db-setup.sh
```
## Software dependencies
Python is needed, Install the vesion mentioned `python-env-setup.sh` else update the setup file with the version installed in the machine.
Execute below to setup python environment and install all the necessary things
```sh
./python-env-setup.sh
```
Install vscode (recommended) along with jupyter extension

# Build and Test
### Recommended
Open the repo in `vscode` once you select the jupyter notebook (`pgvector-hello.ipynb`) choose the kernel on top right corner that start's with `langchain-rag-playpen-`. If it not appeared try reloading the window using (cmd+shift+p) and `reload window` option for osx and (ctrl+shift+p) and `reload window` option for linux.

### OneTime Steps
Uncomment the following line which is there in `pgvector-hello.ipynb` notebook `cell: 6` run once and we can comment as there is no needed to create schema everytime.
```sql
record_manager.create_schema()
```

# Contribute
Feel free to update if it benefits others.