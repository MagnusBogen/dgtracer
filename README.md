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
mk_work_dir
cd ../../../../work/username
rm -rf . // dobbeltsjekk denne kommandoen hehe
git clone ...
cd ...
rm -rf ~/.local/lib/python3.6/site-packages/
rm -rf ~/.local/lib/python2.7/site-packages/
pip3 install PySimpleGUi
pip3 install cv2
pip3 install numpy
```

Run
```bash
python3 event_loop.py
```

### File Structure

The hierarchy should look like this:

    ./
    ├── README.md
    └── src
        ├── configs
        │   └── gui_config.yaml
        ├── gui.py
        ├── program_handler.py
        ├── video.py
        ├── requirements.txt
        ├── files
        │   ├── videos
        │   ├── analyzes
        │   ├── thumbnails
        │   └── graphics
        │       └── logo.png
        └── run.py




## ⛏️ Built Using <a name = "built_using"></a>
- [Python 3.7](https://www.python.org/)


## ✍️ Authors <a name = "authors"></a>
- Magnus Bogen Brurok

