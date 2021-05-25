# Documentation for Developers

## Files

1. `train.py` Main file to train OCR for a given language. Training and network parameters are specified via `.ast` files in the `config/` directory.
```
python3 train.py configs/midlayer.ast configs/len/3.ast
```

## Directories

1. `configs` Contains the training parameters and the network parameters. `default.ast` is loaded by default, other files can be passed in as command line arguments to override default arguments. Each folder has parameters pertaining to individual aspects of the network and training.
    1. `opt` Optimizer
    1. `ilr` Initial Learning Rate
    1. `len` Length of the each slab, width, number of characters, etc.
    1. `lbl` Labelling for the language. For e.g. Telugu can be encoded as a series of Unicode points, as a series of Ligatures, etc.
    1. `mid` Middle Layer (LSTM, GRU, etc.)
    1. `log` Use logarithmic scale for the CTC layer
1. `lab` Experimental code.
1. `rnn_ctc` Code duplicated from [rnn_ctc](https://github.com/rakeshvar/rnn_ctc) repo. Needs to be an external dependency.
1. `data` Sample images.
1. `profile` Profiling training time vs text image generation time.
1. `telugu` or any `<language>`. Can be any language should contain the following information pertaining to the language of interest, e.g. Telugu
    1. `fonts.py` A list of fonts available for that language that can be used for training.
    1. `labeler_*.py` A look up for converting a Unicode language string to a string of labels `{0, 1, 2, ...,  }`. Each labler will have different number of labels. More if you are using ligatures, fewer if you are using unicode as is.
    1. `texter.py` Generates random text from the language. Could be from a corpus or could be from a language model (like one based on bigrams).
1. `tests` Testing files for scribe.
1. `docs` Documentation.
1. `notebooks` Similar to `tests`, `lab`, `profile` directories.
