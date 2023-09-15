
# Generative AI app for note taking

### Secrets
- Update all the `secrets` in the `.streamlit/secrets.toml`

### Install 
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`


### Local Development 
- `source venv/bin/activate`
- Start the app: `streamlit run parse.py` to parse gen ai output in a specific format
- Start the app: `streamlit run eval.py` to generate question and answers and use QAEvalChain to do self evaluation