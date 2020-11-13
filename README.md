<h1 align="center">Disc tracker</h1>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]()
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center">
Gui and Disc tracker using opencv camshift
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
cd dgtracer
```
Check that you have Python 3.8.5. Other versions of python 3 may also work, but not tested.
```bash
python3 --version
```

```bash
pip3 install PySimpleGUi
pip3 install cv2
pip3 install numpy
```

Run
```bash
python3 main.py
```

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
        ├── requirements.txt
        ├── files
        │   ├── videos
        │   ├── analyzes
        │   ├── thumbnails
        │   └── graphics
        │       └── front_picture.png
        └── main.py




## ⛏️ Built Using <a name = "built_using"></a>
- [Python 3.7](https://www.python.org/)


## ✍️ Authors <a name = "authors"></a>
- Magnus Bogen Brurok

