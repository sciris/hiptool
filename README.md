# HealthPrior Tool

The HealthPrior tool, a.k.a. Health Services Prioritization Tool, is a tool for helping optimize health services.

## Install sciris
It is important that you install Sciris and Anaconda Python to get many of the dependencies needed for Numpy and Matplotlib.

## Installing the Python tool

If you are installing these packages for the first time, look at **First time install** below.

Before you install, check that you are using the correct python

`which python`

Should show that you are using Anaconda Python. If it says you are using the built in Python, you need to close down the terminal and open it again. 

To install, do

`python setup.py develop`

in the main folder. 

### If Anaconda Python fails
NOTE: The below steps were used when a failed Aacoda Python install occurred. 
You may need some, all or none of the below. 

If you are starting from a fresh Ubuntu install, you may need to install Python setuptools 

`sudo apt-get install python-setuptools`

`sudo apt-get install python-dev`

`sudo apt install gcc`

Numpy requires cython:
`easy_install --user cython`

Matplotlib requires pkg-config, libfreetype6, and libpng12 

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

Instead of `npm run build` and `python start_server.py`, you can also run 

`bash linux_dev_run`

which runs (in separate terminal windows):

```
python start_dev_server.py
python start_dev_client.py
```

This uses hot reloading, so any changes you make to the client code will be immediately live. Your site will be live at `localhost:8080`.
