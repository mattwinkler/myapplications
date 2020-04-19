virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install --user ipykernel
python -m ipykernel install --user --name=venv

