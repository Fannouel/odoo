FROM odoo:16 

ADD requirements.txt .
RUN pip3 install -r requirements.txt

CMD ["tail", "-f", "/dev/null"]

