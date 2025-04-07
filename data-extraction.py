import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import random

job_link=[]
job_title=[]
available_vs_total_jobs= []
salary= []
place_of_duty= []
grant_date= []
permission_no= []
oep_foreign_employer_details= []
oep_foreign_employer_details_cleaned= []
available_vs_total_jobs_cleaned = []

current_page = 751
proceed=True
while(proceed):
    base_url= f'https://beoe.gov.pk/foreign-jobs?page={current_page}'
    header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
    time.sleep(random.uniform(1, 5))
    # Make an HTTP request to get the page content
    response = requests.get(base_url, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    #if soup.find('div',class_="col-sm-12").text.strip() ==  
    if current_page < 824:
    #soup.find('table',class_='table table-bordered table-striped'): 
        job_listings=soup.find('table',class_='table table-bordered table-striped')

        # extracting columns
        columns= job_listings.thead
        columns= columns.find_all('th')
        fields=[]

        for column in columns:
            field=column.text.strip()
            fields.append(field)
        fields.append("Job Link")

        #extracting data values
        job_listings = job_listings.tbody
        for job in job_listings.find_all('tr'):
            job_link.append(job.find('a').get('href'))
            job_title.append(job.find('a').text.strip())

            job_details =job.find_all('td')

            available_vs_total_jobs.append(job_details[1].text.strip())
            salary.append(job_details[2].text.strip())
            place_of_duty.append(job_details[3].text.strip())
            grant_date.append(job_details[4].text.strip())
            permission_no.append(job_details[5].text.strip())
            oep_foreign_employer_details.append(job_details[6].text.strip())
        
        oep_foreign_employer_details_cleaned = [re.sub(r'\s+', ' ', x.strip()) for x in oep_foreign_employer_details]
        #print(oep_foreign_employer_details_cleaned)

        available_vs_total_jobs_cleaned = [re.sub(r'\s+', ' ', x.strip()) for x in available_vs_total_jobs]
        available_vs_total_jobs_cleaned = [re.sub(r'/', '--', x.strip()) for x in available_vs_total_jobs_cleaned]
        current_page= current_page + 1
    else:
        proceed=False

# Combine data into a DataFrame
df = pd.DataFrame(list(zip(job_title,available_vs_total_jobs_cleaned, salary, place_of_duty, grant_date, permission_no, oep_foreign_employer_details_cleaned, job_link)), columns=fields)
#print(job_title, available_vs_total_jobs, salary, place_of_duty, grant_date, permission_no, oep_foreign_employer_details)
#df=df[available_/_total_jobs].astypr(str)
print(df.head(5))
df.to_csv('imigration_bureau_jobs_p1.csv')
