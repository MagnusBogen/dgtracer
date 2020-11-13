<h1 align="center">Disc tracker</h1>

---

<p align="center">
Gui with object tracer using opencv camshift.
</p>
<br>

## 📝 Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [Authors](#authors)


## 🧐 About <a name = "about"></a>
Tracking of disc from video

## 🏁 Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

```bash
git clone https://github.com/MagnusBogen/dgtracer.git
```
Check that you have Python 3.8.5. Other versions of python 3 may also work, but not tested.
```bash
python3 --version
```
Make a virtual environment.
```bash
python3 -m venv dgTracer_env
cd dgTracer_env/bin
source activate
cd ../..
cd dgtracer
```
Upgrade pip
```bash
pip install --upgrade pip
```
Install requirements
```bash
pip3 install PySimpleGUi
pip3 install opencv-python
```

Run
```bash
python3 main.py
```

A test video can be downloaded here:
https://drive.google.com/drive/folders/1wehdXLM9Nne91L7Y-IYV_3ToiNELzCUn?usp=sharing

### File Structure

The hierarchy should look like this:

    ./
    ├── README.md
    └── src
        ├── gui
        │   ├── gui.py
        │   └── event_loop.py
        ├── program_handler
        │   └── program_handler.py
        ├── video_handler
        │   └── video_handler.py
        ├── files
        │   ├── videos
        │   ├── analyzes
        │   ├── thumbnails
        │   └── graphics
        │       └── front_picture.png
        └── main.py




## ⛏️ Built Using <a name = "built_using"></a>
- [Python 3.8.5](https://www.python.org/)
- [OpenCV 4.4.0.46](https://opencv.org)
- [PySimpleGUI 4.31.0](https://pysimplegui.readthedocs.io/en/latest/)

## ✍️ Authors <a name = "authors"></a>
- Magnus Bogen Brurok

