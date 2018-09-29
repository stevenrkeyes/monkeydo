# monkeydo
AI to play the original Bloon's Tower Defense


# Setup

Install the requirements in requirements.txt:

```shell
# create a .env directory to store virtualenv information, and use python3
virtualenv --python=/usr/bin/python3.5 .env
# activate the virtualenv
source .env/bin/activate
# install the requirements inside the virtualenv
pip install -r requirements.txt
```
In addition to the python requirements in requirements.txt, you will need:
- the flash file "bloonstd_moved.swf" from Ninja Kiwi: http://ninjakiwifiles.com/Games/gameswfs/bloonstd_moved.swf
- the "flashplayer" executable from Adobe
  1. go to https://www.adobe.com/support/flashplayer/debug_downloads.html
  2. download the Flash Player projector
  3. extract the file you download and copy the "flashplayer" executable to the project directory
- tesseract-ocr: `sudo apt-get install tesseract-ocr`

