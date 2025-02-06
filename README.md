# wema-journal
> Forked from [gcallah/demo-repo4](https://github.com/gcallah/demo-repo4)

An app developed by **WEMA** (William, Eric, Matthew, Aaron)

## Progress and Goals
See the following file [here](./ProgressAndGoals.md).

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

#### `.env` settings for MongoDB on the cloud
To use our cloud MongoDB database set `CLOUD_MONGO=1`.
 
#### `.env` settings for MongoDB locally
To use your own local MongoDB database set `CLOUD_MONGO=0`. 

You might have to change `LOCAL_DB_PORT` if your settings are different. The default is `27017`.

On MacOS, to start the service run:
`brew services start mongodb-community`.

To stop the service run: `brew services stop mongodb-community`

### Running the development server
To run the development server, run in terminal:
```./local.sh```


## Production
### Build
To build production, type `make prod`.

The server is hosted on [PythonAnywhere](https://wl2612.pythonanywhere.com/).

# wema-journal-frontend
The frontend can be found here: https://github.com/awu0/wema-journal-frontend
