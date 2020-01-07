command = '/home/ubuntu/fxapp/env/bin/gunicorn'
pythonpath = '/home/ubuntu/code/fxapp/fxapp'
bind = '127.0.0.1:8001'
workers = 3
user = 'ubuntu'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=fxapp.settings'
