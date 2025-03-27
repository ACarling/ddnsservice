FROM python:3.7-alpine

ADD ddns.py .

RUN pip install route53

ENV AWS_ACCESS_KEY=
ENV AWS_ACCESS_SECRET=
ENV A_RECORD_NAME=
ENV POLL_TIMEOUT_SECONDS=5
ENV PYTHONUNBUFFERED=1

CMD [ "python", "-u", "./ddns.py" ]