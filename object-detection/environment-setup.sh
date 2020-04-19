# create and activate virtual environment
virtualenv venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# make sure jupyter can see the installed venv
pip install --user ipykernel
python -m ipykernel install --user --name=venv

