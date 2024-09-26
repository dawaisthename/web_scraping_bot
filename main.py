from bs4 import BeautifulSoup
import requests
import time
#personal skills
my_skills =['coding','programming','python','react','html', 'css',
            'javascript','django', 'django rest framework', 'mysql',
            'postgresql', 'sqlite']
#to track of the jobs already posted
printed_jobs = set()


def find_job():
    #make a request to the url
    html_text = requests.get(
        'https://www.timesjobs.com/candidate/job-search.'
        'html?searchType=Home_Search&from=submit&asKey='
        'OFF&txtKeywords=&cboPresFuncArea=35').text

    soup = BeautifulSoup(html_text, 'lxml') #parse the returned file
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')#find each job elements


    for job in jobs:
        more_info = job.header.h2.a['href']

        #check if the job is already posted
        if more_info not in printed_jobs:
            job_published = job.find('span', class_='sim-posted').span.text
            if 'Posted today' in job_published:
                job_skills = job.find('span', class_="srp-skills").text.strip().split('\n')

                skill_status = False #Reset skill status for each job
                for my_skill in my_skills:
                    for job_skill in job_skills:
                        if my_skill in job_skill:
                            skill_status = True
                            break
                    if skill_status:
                        break
                #if job matches the skills print them out
                if skill_status:
                    job_company = job.find('h3', class_="joblist-comp-name").text
                    print(f'company name: {job_company.strip()}')
                    print(f"skills_needed: {job_skills}")
                    print(f'more Info:{more_info}')
                    print('\n')
                    #add job url to the printed jobs
                    printed_jobs.add(more_info)


if __name__ == "__main__":
    while True:
        find_job()
        print('waiting for a new job...')
        time.sleep(60)


