FROM python:3.12.0a6-bullseye

RUN mkdir -p /home/app

COPY setup.py setup.py
RUN pip3 install .

COPY . .

CMD ["flask", "--app", "world_spc", "--debug", "run", "--host=0.0.0.0"]
