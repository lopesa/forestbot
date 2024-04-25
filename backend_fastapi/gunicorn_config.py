'''
https://stackoverflow.com/questions/63424042/call-missing-1-required-positional-argument-send-fastapi-on-app-engine

have to add "--worker-class uvicorn.workers.UvicornWorker"
in Digital Ocean app engine startup command, for it to work

underlying cause maybe:
App Engine requires your main.py file to declare an app variable which corresponds to a WSGI Application.
Since FastAPI is an asynchronous web framework, it is not compatible with WSGI (which is synchronous).
Your best option would be to use a service like Cloud Run, which would allow you to define your own runtime and use an asynchronous HTTP server compatible with FastAPI.

but the hack(?) seems to work
'''

bind = "0.0.0.0:8080"
workers = 2
