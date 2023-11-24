FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY streamlit_app.py .

CMD ["streamlit", "run", "streamlit_app.py"]
