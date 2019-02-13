# HIPtool

The HIPtool, a.k.a. Health Interventions Prioritization Tool, is a tool for helping optimize health services.

## Quick start guide

1. Install `hiptool` by typing `python setup.py develop` in the root folder.

2. Change to the `client` subfolder and type `fullrun`.

3. If it worked, go to `localhost:8091` in your browser to use the webapp.

## Slow start guide

1. Clone the `hiptool` repository (yes, this one!).

2. Install `hiptool` by typing `python setup.py develop` in the root folder.

3. Test that you can import it by typing `import hiptool`, e.g.
```
>>> import hiptool
ScirisWeb 0.12.2 (2019-02-11) -- (c) Sciris.org
DataStore loaded at redis://127.0.0.1:6379/5 with temp folder /tmp/tmpwonYy_
HIPtool 2.0.0 (2019-02-13)
>>>
```

4. Test that plotting works with `python -i scripts/example.py`, which should bring up a graph.

5. To build and start the webapp, change to the `bin` folder, and type `python run.py`. Note: this will take a lot of time (up to 15 min), especially on a first run!

6. If it worked, you can go to `localhost:8091` in your browser and see the HealthPrior webapp.

7. If it didn't work, try each of the steps separately:

  8a. Type `python install_client.py` to install the JavaScript modules. You should see output like this:
  ```
  your_computer:~/hiptool/bin> python install_client.py
  npm WARN optional Skipping failed optional dependency /karma/chokidar/fsevents:
  npm WARN notsup Not compatible with your operating system or architecture: fsevents@1.1.3
  npm WARN optional Skipping failed optional dependency /chokidar/fsevents:
  npm WARN notsup Not compatible with your operating system or architecture: fsevents@1.1.3
  ```

  Don't worry about `WARN`, but _do_ worry about `ERR`! If you see `ERR`, that means that installation failed.

  8b. Type `python build_client.py` to build the JavaScript app. You should see output like:
  ```
  static/img/ucl-logo-transparent.png    35.5 kB          [emitted]         
     static/img/world-bank-logo.png    30.7 kB          [emitted]         
    static/mpld3.v0.3.1.dev1.min.js    37.6 kB          [emitted]         

  Build complete.

  Tip: built files are meant to be served over an HTTP server.
  Opening index.html over file:// won't work.
  ```
  You should not see any warnings or errors on this step.

  8c. Type `python run.py` to start the server running. You should see something like:
  ```
>> Webapp initialization complete (elapsed time: 0.00 s)
Matplotlib backend switched to "Agg"

      ___  ___                                                            
     / __|/ __|   ===================================================     
     \__ \ |__    ScirisApp "HealthPrior" is now running on port 8091     
     |___/\___|   ===================================================     
                                                                          

  ```

9. If that all worked, happy health-prioritizing!

**Please see the README in the `bin` folder for more options for how to run HealthPrior.**


## Detailed installation instructions for Windows

No known issues; please use the quick start guide above.

## Detailed installation instructions for Linux

No known issues; please use the quick start guide above.

## Detailed installation instructions for Mac
1. In the root `pyenv` folder (see Sciris instructions), clone [hiptool](https://github.com/sciris/hiptool.git)

2. Install `hiptool` by typing `python setup.py develop` in the `pyenv/hiptool` folder.

3. Change to the `bin` subfolder and type `pythonw run.py`.

4. If it worked, go to `localhost:8091` in your browser to use the webapp.
