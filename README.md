# HealthPrior Tool

The HealthPrior tool, a.k.a. Health Services Prioritization Tool, is a tool for helping optimize health services.

## Quick start guide

1. Install [Sciris](http://github.com/optimamodel/sciris).

2. Install `hptool` by typing `python setup.py develop` in the root folder.

3. Change to the `bin` subfolder and type `python run.py`.

4. If it worked, go to `localhost:8091` in your browser to use the webapp.

## Slow start guide

1. Install [Sciris](http://github.com/optimamodel/sciris) and follow all installation instructions there.

2. Clone the `hptool` repository (yes, this one!).

3. Install `hptool` by typing `python setup.py develop` in the root folder.

4. Test that you can import it by typing `import hptool`, e.g.
```
>>> import hptool
HealthPrior 0.2.9 (2018-03-26)
Sciris v0.3 (2018-03-23) loaded for local use (display=:0)
>>>
```

5. Test that plotting works with `python -i scripts/example.py`, which should bring up a graph.

6. To build and start the webapp, change to the `bin` folder, and type `python run.py`. Note: this will take a lot of time (up to 15 min), especially on a first run!

7. If it worked, you can go to `localhost:8091` in your browser and see the HealthPrior webapp.

8. If it didn't work, try each of the steps separately:

  8a. Type `python install_client.py` to install the JavaScript modules. You should see output like this:
  ```
  your_computer:~/hptool/bin> python install_client.py
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

  8c. Type `python start_server.py` to start the server running. You should see something like:
  ```
  >> Doing other scirismain-specific initialization...
  -- Welcome to the HealthPrior webapp, version 0.2.9 (2018-03-26) --
  Site starting on 8091
  Starting factory <twisted.web.server.Site instance at 0x7fedcb347dd0>
  ```

9. If that all worked, happy health-prioritizing!

**Please see the README in the `bin` folder for more options for how to run HealthPrior.**


## Detailed installation instructions for Windows

No known issues; please use the quick start guide above.

## Detailed installation instructions for Linux

No known issues; please use the quick start guide above.

## Detailed installation instructions for Mac
1. Follow the Mac installation instructions for [Sciris](http://github.com/optimamodel/sciris).

2. In the root `pyenv` folder (see Sciris instructions), clone [HPTool](https://github.com/optimamodel/hptool.git)

3. Install `hptool` by typing `python setup.py develop` in the `pyenv/hptool` folder.

4. Change to the `bin` subfolder and type `pythonw run.py`.

5. If it worked, go to `localhost:8091` in your browser to use the webapp.
