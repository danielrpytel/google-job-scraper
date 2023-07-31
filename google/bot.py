from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import os
import time


class Bot():

    def __init__(self):
        print("Opening Chrome...")
        self.driver = webdriver.Chrome()

    def _get_all_jobs(self, jobTitle):
        requirements_url = self._get_requirements_url()
        query = f"https://www.google.com/search?q={jobTitle}&ibp=htl;jobs#htivrt=jobs&{requirements_url}".replace(
            " ", "+")
        self.driver.get(query)
        time.sleep(1)
        processed_jobs = set()
        jobs_data = []

        while True:
            listings = self.driver.find_elements(
                By.XPATH, ".//div[@class='PwjeAc']")

            new_jobs_found = False

            for listing in listings:
                if listing not in processed_jobs:
                    self._scroll_into_view(listing)
                    listing.click()

                    processed_jobs.add(listing)
                    new_jobs_found = True
                    data = self._get_job(listing)
                    identifier = self._create_job_identifier(data)
                    data.update(identifier)
                    jobs_data.append(data)
                    time.sleep(.5)

            if not new_jobs_found:
                break

        return jobs_data

    def _create_job_identifier(self, job_data):
        # Create a unique identifier for a job posting using its properties
        identifier = f"{job_data['title']}_{job_data['company_name']}_{job_data['location']}_{job_data['description']}"
        return {"identifier": identifier}

    def _get_job(self, listing):

        return {
            "title": self._get_job_title(listing),
            "company_name": self._get_job_company(listing),
            "location": self._get_job_location(listing),
            "description": self._get_job_description(),
            "posting_url": self._get_job_url(),
        }

    def _get_job_title(self, listing):
        title = listing.find_element(
            By.XPATH, ".//div[@class='BjJfJf PUpOsf']").text
        return title

    def _get_job_company(self, listing):
        company = listing.find_element(
            By.XPATH, ".//div[@class='vNEEBe']").text
        return company

    def _get_job_location(self, listing):
        location = listing.find_element(
            By.XPATH, ".//div[@class='Qk80Jf']").text
        return location

    def _get_job_description(self):
        try:
            description_container = self.driver.find_element(
                By.XPATH, ".//div[@class='whazf bD1FPe']")
            expand_description_button = description_container.find_element(
                By.XPATH, ".//div[@class='CdXzFe j4kHIf']")
            self._scroll_into_view(expand_description_button)
            expand_description_button.click()
            time.sleep(.3)
        except NoSuchElementException:
            pass

        if description_container:
            description = description_container.find_element(
                By.XPATH, ".//span[@class='HBvzbc']").text
            return description
        else:
            return ""

    def _get_job_url(self):
        posting_url = self.driver.current_url
        return (posting_url)

    def _scroll_into_view(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", element)

    def _get_requirements_url(self):
        experience_option1 = "requirements:no_experience"
        experience_option2 = "requirements:years3under"
        date_posted_option1 = "date_posted:today"
        date_posted_option2 = "date_posted:3days"

        # choose options to add to the url link
        url_options = f"&htichips={experience_option1},{date_posted_option1}"

        return url_options


# first htischips then you can divide requirements with comma htichips=requirements:no_experience,date_posted:today
# &htichips=date_posted:today / 3days
# &htichips=requirements:no_experience / years3under
