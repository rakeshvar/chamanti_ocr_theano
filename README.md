# Chamanti OCR in Theano చామంతి

# Discontinued
As `theano` has been discontinued and `TensorFlow` has taken over. I am moving this project to 
TensorFlow. So this work is discontinued. Code duplication from the `rnn_ctc` library for 
`Reccurent Nueral Networks` with `Connectionist Temporal Classification` has been deleted.
The code for 'scribe'ing Indian Language Text has also been moved to a new package  
[IndicScribe](https://github.com/rakeshvar/IndicScribe)

# TensorFlow Package
The Chamanti OCR based on `TensorFlow` and `IndicScribe` will be up in my repositories.

# Mission
This project aims to build a very ambitious OCR framework, that should work on any language.
It will not rely on segmentation algorithms (at the glyph level), making it ideal for highly
agglutinative scripts like Arabic, Devanagari etc. We will be starting with Telugu however.
The core technology behind this is going to be Recurrent Neural Networks using CTC from
the repo [rnn_ctc](https://github.com/rakeshvar/rnn_ctc).

# Python Dependencies
1. numpy
1. scipy
2. theano

# My other packages
1. [rnn_ctc](https://github.com/rakeshvar/rnn_ctc)
2. [IndicScribe](https://github.com/rakeshvar/IndicScribe)


You can read the [developer documentation](README_DEVELOPER.md) for more details about the code and configurations.
