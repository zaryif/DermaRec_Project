install required library

command line> pip install fastapi
command line> pip install uvicorn
command line> pip install requests

Requests module detail => https://www.w3schools.com/python/module_requests.asp

start api services (derma_rec_server.py)

command line> uvicorn derma_rec_server:my_app --reload

=> run api client to acquire the services. (derma_rec_client.py)

command line> python3 derma_rec_client.py
