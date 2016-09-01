# చామంతి

# Mission
This project aims to build a very ambitious OCR framework, that should work on any language. It
will not rely on segmentation algorithms (at least at the glyph level),
making it ideal for highly agglutinative scripts like Arabic, Devanagari etc. We will be starting
 with Telugu however. The core technology behind this is going to be Recurrent Neural Networks
 using CTC. The support for this will be coming from the repo [rnn_ctc](https://github.com/rakeshvar/rnn_ctc).

# Code so far
Date `2016, Mar, 8`

1. `akshara_regexp`:  Regular expression to split a Telugu sentence into aksharas(syllables).
2. `cffi_wrapper.py`: A wrapper around functions to render text to images. (Uses cairo via cffi)
3. `indic_scribe.py`: Uses cffi_wrapper to render given text to image.
4. `linedraw.py`: Class wrapper around indic_scribe and a labeler.
5. `print_utils.py`
6. `scribe_corpus.py`: Given a corpus of unicode text. It will write each line to an image and
save the numpy arrays. Uses `indic_scribe`.
7. `telugu_fonts.py`: List of telugu fonts and their properties.
8. `telugu_labeler_basic.py`: A labler, takes a string of unicode text and returns a sequence of
labels. These labels could be at the akshara level or unicode character level or at an intermediate
level. The basic labeler just returns one label for each unicode character.
9. `line_seperate.py`: Detects lines in a binary text image.

# Setup

Clone this repo and run installation script.

```
git clone https://github.com/rakeshvar/chamanti_ocr
cd chamanti_ocr
./scripts/install.sh
```

For now you can see if `scribe.py` is working properly by running it as
```sh
python3 scribe.py <(echo 'క్రైః') > kraih.txt
```
The output should contain the text rendered in various fonts!

* You can get the various fonts from [this repo](https://github.com/TeluguOCR/Fonts). Just copy all the fonts to your `~/.fonts` directory.



# Troubleshooting

You should have `libffi`, `cffi` and `cairocffi` installed. These are constantly changing and are works in
progress. More over you might need root privileges to install libraires.

If `cffi` is complaining that it needs `libffi` then *try* to install it as

```sh
sudo apt-get install libffi-dev
# OR
yum install libffi
```

But then if you are not root on an RHEL machine (which is the case if you are on a server) then

```sh
mkdir ~/software/
cd ~/software/
wget ftp://sourceware.org/pub/libffi/libffi-3.2.1.tar.gz
tar -xvf libffi-3.2.1.tar.gz
cd libffi-3.2.1/
./configure --prefix=/home/<NAME>/usr
make -j4
make check
make install
```

Open `.bashrc` file and add these lines

```
export PATH=$PATH:~/usr/bin:~/software/eclipse
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/usr/lib:~/usr/lib64
export C_INCLUDE_PATH=$C_INCLUDE_PATH:~/usr/include:~/usr/lib/libffi-3.2.1/include
export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:~/usr/include:~/usr/lib/libffi-3.2.1/include
```

Try installing those packages again

```sh
LDFLAGS=-L/home/<NAME>/usr/lib64 pip3 install cffi==0.8.6
pip3 install cairocffi==0.6
```

## Other Problems
* If your PIL / Pillow is not able to open tiff image files.
Follow this: http://stackoverflow.com/a/10109941
If you do not have root priveleges are installing `libtiff` etc. locally,
make sure your `LD_LIBRARY_PATH` points to something like `~/usr/lib` that has `libtiff` etc.
