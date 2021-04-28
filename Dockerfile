FROM python:slim
RUN pip install flask flask_restful flask_sqlalchemy PyMySQL[rsa] gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:80", "app:create_app()"]
