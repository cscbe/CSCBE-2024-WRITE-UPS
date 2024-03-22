from time import sleep

url = "http://localhost:80/"
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import db
import os

options = Options()
options.headless = True
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

driver.get(url)
driver.add_cookie({"name": "session", "value": os.environ["FLAG"]})

print("Starting", flush=True)

while True:
    # try:
    unapproved_particles = db.get_unapproved_particles()
    if len(unapproved_particles) > 0:
        print(f"Unapproved particles: {db.get_unapproved_particles()}", flush=True)
        for particle in db.get_unapproved_particles():
            driver.get(url + "particles/" + particle["uuid"])
            db.mark_particle_approved(particle["uuid"])
    else:
        print(f"No new particles to approve", flush=True)
    sleep(2)


driver.quit()
