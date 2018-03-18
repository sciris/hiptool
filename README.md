# HealthPrior Tool

The HealthPrior tool, a.k.a. Health Services Prioritization Tool, is a tool for helping optimize health services.

## Install sciris


## Installing the Python tool

If you are installing these packages for the first time, look at **First time install** below.

To install, do

`python setup.py develop`

in the main folder. 

### First time install
If you are starting from a fresh Ubuntu install and have not used 
You may need to install Python setuptools 

`sudo apt-get install python-setuptools`

`sudo apt-get install python-dev`

Numpy requires cython:
`easy_install --user cython`

Matplot lib requires pkg-config, libfreetype6, and libpng12 

`sudo apt-get install pkg-config`

`sudo apt-get install libfreetype6-dev`

`sudo apt-get install libpng12-dev` 

EXCEPT: Ubuntu killed this library, so you need to get it here: https://packages.ubuntu.com/xenial/i386/libpng12-0/download

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

This uses hot reloading, so any changes you make to the client code will be immediately live. Your site will be live at `localhost:8080`.
