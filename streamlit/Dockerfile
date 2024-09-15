FROM python:3.8-slim

WORKDIR /streamlit

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD [ "streamlit", "run", "Dashboard.py" ]