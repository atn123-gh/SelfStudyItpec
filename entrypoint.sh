#!/bin/bash
export DJANGO_DEBUG="True"
python3 itp_project/manage.py makemigrations --noinput --settings=itp_project.settings.production
python3 itp_project/manage.py migrate --run-syncdb --noinput --settings=itp_project.settings.production
python3 itp_project/manage.py collectstatic --noinput --settings=itp_project.settings.production
python3 itp_project/manage.py init_rdbms --settings=itp_project.settings.production
python3 itp_project/manage.py init_noSql --settings=itp_project.settings.production
# python3 itp_project/manage.py insertsolutions

##環境変数のDEBUGの値がTrueの時はrunserverを、Falseの時はgunicornを実行します
if [ "$DJANGO_DEBUG" = "True" ] # to $default_server = True
then
    echo "local-----------"
    python itp_project/manage.py runserver 0.0.0.0:8000
else
    # gunicornを起動させる時はプロジェクト名を指定します
    # 今回はdjangopjにします
    gunicorn itp_project.wsgi --bind 0.0.0.0:8000  --chdir /code/itp_project
fi
