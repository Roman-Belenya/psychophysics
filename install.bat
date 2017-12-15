echo off

pip install virtualenv

virtualenv env
call env/scripts/activate

pip install pypiwin32 wxPython install numpy scipy matplotlib pandas pyopengl pyglet pillow moviepy lxml openpyxl xlrd configobj pyyaml gevent greenlet msgpack-python psutil tables requests[security] pyosf cffi pysoundcard pysoundfile seaborn psychopy_ext python-bidi future json-tricks psychopy
