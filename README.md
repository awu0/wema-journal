# wema-journal
> Forked from [gcallah/demo-repo4](https://github.com/gcallah/demo-repo4)

An app developed by **WEMA** (William, Eric, Matthew, Aaron)

## Development
### Installing for development
Use a virtual environment to install the packages:

1. Create the virtual environment
```python3 -m venv venv```
2. Activate the environment
```source venv/bin/activate```
3. Run `make dev_env` to install the developer dependencies

### Setting the enviroment variables
Put the secret `.env` file in the root directory.

### Running the development server
To run the development server, run in terminal:
```./local.sh```


## Production
### Build
To build production, type `make prod`.
