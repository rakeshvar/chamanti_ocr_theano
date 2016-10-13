# చామంతి

# Mission
This project aims to build a very ambitious OCR framework, that should work on any language.
It will not rely on segmentation algorithms (at the glyph level), making it ideal for highly
agglutinative scripts like Arabic, Devanagari etc. We will be starting with Telugu however. 
The core technology behind this is going to be Recurrent Neural Networks using CTC from 
the repo [rnn_ctc](https://github.com/rakeshvar/rnn_ctc).

# Dependencies
1. numpy
1. scipy
2. theano
3. libffi
4. cffi
5. cairocffi

# Setup

Clone this repo and run installation script.

```
git clone https://github.com/rakeshvar/chamanti_ocr
cd chamanti_ocr
./scripts/install.sh
```

## Fonts 
You will need a lot of fonts for a language you want to train on. 
You can get numerous Telugu fonts from [here](https://github.com/TeluguOCR/Fonts). 
Just copy all the fonts to your `~/.fonts` directory.

# Running

## Checking
Given the complicated dependencies, you can first check if you have all the dependencies as

```sh
cd tests
python3 test_scribe_random.py
python3 test_scribe_all_fonts.py <(echo 'క్రైః') > kraih.txt
# The output should contain the text rendered in various fonts
```

## Training an RNN
You can now train an RNN to read Telugu! Although you can not save it yet!

```sh
python3 train.py
```

# Troubleshooting

## Dependencies 

You should have `libffi`, `cffi` and `cairocffi` installed. 
These are constantly changing and are works in progress. 
More over you might need root privileges to install libraries (libffi).

If `cffi` is complaining that it needs `libffi` then try to install it as

### Ubuntu

```sh
sudo apt-get install libffi-dev
```

### RHEL, CentOS

```sh
yum install libffi
```

But then if you are **not** root on an RHEL machine (which is the case if you are on a server) then
try

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
export PATH=$PATH:~/usr/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/usr/lib:~/usr/lib64
export C_INCLUDE_PATH=$C_INCLUDE_PATH:~/usr/include:~/usr/lib/libffi-3.2.1/include
export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:~/usr/include:~/usr/lib/libffi-3.2.1/include
```

Try installing those packages again

```sh
LDFLAGS=-L/home/<NAME>/usr/lib64 pip3 install cffi
pip3 install cairocffi
```

## Other Problems
* If your PIL / Pillow is not able to open tiff image files.
Follow this: http://stackoverflow.com/a/10109941
If you do not have root priveleges are installing `libtiff` etc. locally,
make sure your `LD_LIBRARY_PATH` points to something like `~/usr/lib` that has `libtiff` etc.
