# BirdIdentifier
A website to identify 20 most common UK birds using a CNN trained on a dataset of 3000 images. Data taken from https://www.kaggle.com/code/davemahony/2-20-uk-garden-bird-ds-prep-with-imagelabs. 

In order to run, you need to run model.py and save it as model.h5. This allows for the weights to be pulled through to the application. I have also uploaded the model.py which gets updated to improve accuracy. Updated model using batch norm coming soon. On validation sets, I have reached ~83% and on real life data, i.e. videos from Youtube etc. it is lower which needs improving! 

Video classification has also been added with the return a JSON output of a prediction per frame which needs object tracking added (unfortunately).

Once you have your model.h5 file, you need to cd to the file path, i.e. in my case, its WhatsInMyGarden.
Then,

``` python app.py ```

and it will run on a local server.

**Warning:** If, like me, you have an M1 chip device, you may encounter "Hardware problems" upon running. See https://stackoverflow.com/questions/65383338/zsh-illegal-hardware-instruction-python-when-installing-tensorflow-on-macbook or consider installing a Flask environment which worked for me.
