# HPP Tool

The Health Packages Prioritization Tool, a.k.a. Health Services Prioritization Tool, a.k.a., E3UHC, is a tool for helping optimize health services.

**WARNING, copied from Sciris**


## Installation and Run Instructions

### Installing on Linux Systems

[needs to be written...]

### Installing on Windows Systems

#### GitHub Repo Dependencies

In addition to cloning this repo, users will need to to clone the latest
code from the `sciris` repo which can be found
[here](https://github.com/optimamodel/sciris) and they need to follow
the full installation directions there.  (This includes instructions for
package dependencies and for installation of Redis.)

#### Setup of Config File

`sciris\sessionmanager\config.py` is initially set up as a copy of `config_v2.py`.  
You want to copy the version of `config.py` in this repo to overwrite that in
the `sciris` repo.  Then you should set the absolute paths to your local sciris
repo in the `CLIENT_DIR` and `WEBAPP_DIR` lines of the file, so that the `sciris`
repo can find the correct versions of the client and webapp.

#### Initial Build of the Client

After cloning or pulling this repo, use the following steps to do the
initial build of the app:
* `cd vueinterface`
* `npm install` builds the Node modules the app uses.  This step can take
a few minutes to complete.
* `npm run build` generates the build version of the app.

#### Running the App

See the [Sciris repo directions](https://github.com/optimamodel/sciris) for
directions on how to run the app, either from the build version or using
the dev server.  The app is built and run from the `sciris` repo, not the
`hpptool` repo.

### Installing on Mac OSX Systems

[needs to be written...]
