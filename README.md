# HealthPrior Tool

The HealthPrior tool,a.k.a. Health Services Prioritization Tool, is a tool for helping optimize health services.


## Installing the Python tool

To install, do

`python setup.py develop`

in the main folder.

## Installing the client

In the `client` folder, run

```
npm install
npm run build
```

## Refreshing the client

If you have made changes to the frontend, you will need to do `npm run build` again.

## Starting the server

In the `webapp` folder, run

`python start_server.py`

This will start on port `localhost:8091`.

## Development mode

Instead of `npm run build` and `python start_server.py`, you can also run (in separate terminal windows):

```
python start_dev_server.py
python start_dev_client.py
```

This uses hot reloading, so any changes you make to the client code will be immediately live.
