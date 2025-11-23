SETUP & RUN INSTRUCTIONS


STEP 1: Install Required Libraries

command line> pip install fastapi
command line> pip install uvicorn
command line> pip install requests

Requests module detail => https://www.w3schools.com/python/module_requests.asp

STEP 2: Start the Server

Open Terminal and run these commands:
command line>  cd Desktop/DermaRec_Project
command line>  python3.13 -m uvicorn derma_rec_server:my_app --reload

Note: Keep this terminal window OPEN while using the app.

STEP 3: Run the Client

Open a NEW terminal window and run these commands:
command line> cd Desktop/DermaRec_Project
command line> python3.13 derma_rec_client.py

STEP 4: View Logs

command line> cd Desktop/DermaRec_Project
command line> cat derma_log.txt
