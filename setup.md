pip cache purge

rm -rf .venv

python3.11 -m venv venv
source .venv/bin/activate

source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

source .venv/bin/activate
streamlit run app/streamlit_app.py