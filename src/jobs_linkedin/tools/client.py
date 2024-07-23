import os
import urllib
from selenium.webdriver.common.by import By

from .driver import Driver


class Client:
    def __init__(self):
        url = 'https://linkedin.com/'
        cookie = {
            "name": "li_at",
            "value": os.environ["LINKEDIN_COOKIE"],
            "domain": ".linkedin.com"
        }

        self.driver = Driver(url, cookie)

    def find_jobs(self, position):
        positions = [position]
        results = []
        if ',' in position:
            positions = position.split(',')
        
        for position in positions[:1]: # TODO use all lists I'm adding [:1] to decrease OPENAI costs
          encoded_string = urllib.parse.quote(position.lower())
          url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_string}&origin=JOBS_HOME_KEYWORD_HISTORY&refresh=true"
          self.driver.navigate(url)

          job_elements = self.driver.find_elements(
              By.XPATH, "//a[contains(@href, '/jobs/view/')]")
          
          print(f"Job Elements {job_elements}")
          job_links = []
          for job_element in job_elements:
              print("##############")
              print(f"Job Element {job_element}")
              try:
                  job_link = job_element.get_attribute("href")
                  job_links.append(job_link)
              except Exception as e:
                  print(e)
                  continue
          print(job_links)
          for job_link in job_links[:10]:
              try:
                  print("##############")
                  print(f"Navigating to {job_link}")
                  self.driver.navigate(job_link)

                  # Locate the company name and link e.g. Uber - https://www.linkedin.com/company/uber/
                  company_elements = self.driver.find_elements(
                      By.XPATH, "//div[@class='job-details-jobs-unified-top-card__company-name']/a")
                  # get the first element
                  print(f"Company Elements {company_elements}")
                  company_element = company_elements[0]
                  print(f"Company Element {company_element}")
                  company_name = company_element.text.strip()
                  company_link = company_element.get_attribute("href")
                  print(f"Company Name {company_name}")
                  print(f"Company Link {company_link}")

                  # find the competency match, e.g. "7 de 10 competências correspondem ao seu perfil"
                  job_insights_elements = self.driver.find_elements(
                      By.XPATH, "//button[@class='job-details-jobs-unified-top-card__job-insight-text-button']/a")
                  job_insights_element = job_insights_elements[0]
                  print(f"Job Insights Element {job_insights_element}")
                  competency_match = job_insights_element.text.strip()
                  print(f"Competency Match {competency_match}")

                  # find company description
                  job_details_elements = self.driver.find_elements(
                      By.XPATH, "//div[@id='job-details']/div")
                  print(f"Job Details Elements {job_details_elements}")
                  job_details_element = job_details_elements[0]
                  print(f"Job Details Element {job_details_element}")
                  job_description = job_details_element.text.strip()
                  print(f"Job Description {job_description}")

                  result = {}
                  result["name"] = company_name
                  result["link"] = company_link
                  result["description"] = job_description
                  result["proficiency_match"] = competency_match
                  print(result)
              except Exception as e:
                  print(e)
                  continue
              results.append(result)
        return results

    def close(self):
        self.driver.close()
