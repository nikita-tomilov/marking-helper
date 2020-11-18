# marking-helper
A helper for marking Bessmertny's data for the IDA university course.

## Requirements
- python 3.6+
- flask

## How-to

1. Setup the ```DATASET_FOLDER``` environment variable to point to the dataset folder.
For example,
```
export DATASET_FOLDER=/home/user/dataset/1
```
2. Start the program
```
python3 main.py
``` 
or 
```
export FLASK_APP=main.py
flask run
```
3. Navigate your browser to ```127.0.0.1:5000``` and start marking up the data.

## Known problems
- If there is a ```.jpg``` file in the dataset entry, but the file itself is invalid, the iframe having the link wont't show
- A number of websites (theoretically, ones with HSTS enabled) won't show up in the iframe if there is no jpg file
