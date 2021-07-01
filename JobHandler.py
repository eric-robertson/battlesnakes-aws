# Simple file to assign jobs to various threads for processing
# Currently doesnt do threading, but should be easy to add i hope

import threading
import time

jobs = []
threads = []

def create_job ( i ):
    jobs.append( i )

def claim_job ( ):
    return jobs.pop(0)
