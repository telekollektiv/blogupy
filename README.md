# blogupy

> Yo dawg, we need a static blog system for an art project

This system is in use as blog during the Basel (CH) based [ATOPIE](https://atopie.net) Art project. It's running as an open blog that welcomes anybody to submit their content without registration.

It features:

* File based database - exportable and versionable with git
* (Limited) Markdown support
* Announce your events
* Open content submission
* A moderation interface (you better http auth that, btw)
* Full support for js disabled browsers

## How to install?

Make sure you're using a proper operating system and the following installed is installed:

* git
* python
* python-pip
* python-virtualenv
* bower

Next:

1. `git clone https://github.com/telekollektiv/blogupy.git`
2. `cd blogupy/`
3. `virtualenv .`
4. `. bin/activate`
5. `pip install -r requrements.txt`
6. `bower install`
7. `./blogu.py` # for development
8. `pip install gunicorn`
9. `./bin/gunicorn blogu:app` # for production

## Future plans

None

# Legal fineprint

The name of this project, blogupy, is entirely fictional. Any resemblance to other projects or movements is purely coincidental.

## License

blogupy is free software in the terms of the GPLv3 licence.

## Font licenses

Some fonts in this project are under different licenses. Take a look at these files: font_licence1.txt, font_licence2.txt (to be added soon)
