# BirdIdentifier
A website to identify 20 most common UK birds using a CNN trained on a dataset of 3000 images. Data taken from https://www.kaggle.com/code/davemahony/2-20-uk-garden-bird-ds-prep-with-imagelabs. 

In order to run such file, you need to structure the files as follows: 
WhatsInMyGarden/
├── app.py    # Your Flask application code
├── model.h5   # Trained model file
├── templates/           # Directory for HTML templates
│   ├── index.html       # HTML template for the front page
│   └── result.html     # HTML template for the results page
├── static/              # (TBC)
│   └── style.css        # CSS styling for my template
├── BirdImages/          # Directory containing your bird images
│   ├── Blackbird/
│   ├── Bluetit/
│   ├── ... (other bird categories)
├── venv/                 # Your virtual environment (if you need one (See later on))
└── bird_classifier.py/    # code that pulls through the weights from my model.

I have also uploaded the model.py where the .h5 stems from for further understanding of model/if anyone has improvements.

You need to cd to the file path, i.e. in my case, its WhatsInMyGarden.
Then, 
```
python app.py
 and it will run on a local server.

**Warning:** If, like me, you have an M1 chip device, you may encounter "Hardware problems" upon running. See https://stackoverflow.com/questions/65383338/zsh-illegal-hardware-instruction-python-when-installing-tensorflow-on-macbook or consider installing a Flask environment which worked for me.
