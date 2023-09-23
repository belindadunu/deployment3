# Improving the Reliability of Our URL Shortener 

Welcome back! In our [last deployment](https://github.com/belindadunu/jenkins-eb-deploy), we created a Jenkins pipeline to automatically build, test and deploy our URL shortener application from GitHub to Elastic Beanstalk. We also created a GitHub webhook to trigger this pipeline on code changes.

Now that we have a working deployment application, we want to improve reliability as we offer it as a service.

## The Story

We are a tech start-up with a URL shortener service. We have a service level agreement (SLA) with Nike to provide access to our tool.

An SLA is like a customer service guarantee for services. For example, just like a restaurant promises to bring your food within a certain time, we promise a certain uptime and reliability.

Our SLA with Nike allows only 20 minutes of downtime per year. If anything happens, we must communicate the incidents to Nike.
 
## Incident Scenario
-----------------------------------------
A new hire deployed version 2 of the app by committing directly to the main branch. This triggered an automatic deploy that replaced version 1 in production.

The site then went down for 10 minutes, triggering an email alert. 

<img width="732" alt="Screen Shot 2023-09-23 at 8 22 07 AM" src="https://github.com/belindadunu/deployment3.1/assets/139175163/112ccbae-d638-4ea5-8ab7-e1e256b81e59">

## Postmortem - URL Shortener Outage

### Overview
    - Date - September 21, 2023
    - Authors - Belinda Dunu
    - Status - Completed

This incident was detected when an `ERROR` log appeared in our ElasticBeanstalk environment and was triggered and the DevOps team were notified. 

### Summary
    - Duration - The outage lasted 10 minutes
    - Impact - Unable to access URL shortener during window
    - Root Causes - Deployed faulty version 2 code that crashed service

### Timeline
    - 1:05 PM - Faulty code deployed, crashing service
    - 1:07 PM - Monitoring alerts of outage received
    - 1:10 PM - Rolled back code to restore service
    - 1:15 PM - Service restored, root cause identified

### Root Causes
    - Version 2 contained regression error in JSON parsing logic
    - Lacked sufficient testing before deploying new version

**Resolution steps:** Checked monitoring, logs, and git to identify the recent deployment. 

To roll back, we first ran `git log --oneline` to view recent commits. We saw version 2 had been merged into the main branch.

<img width="908" alt="Screen Shot 2023-09-22 at 11 05 09 AM" src="https://github.com/belindadunu/deployment3.1/assets/139175163/b2eadb0b-089b-43c6-aef2-7da69b395787">

We initially thought of troubleshooting but that would take an unknown amount of time to figure out the root cause. We decided to complete a rollback for the meantime then go back to troubleshoot after.

To rollback, we could have checked out the main branch again, but that would still contain the faulty v2 code.

Instead, we wanted to rollback specifically to the last known good commit of version 1. we checked the hash of the v1 commit we wanted to revert to.

We then ran `git checkout -b <branch name> <commit hash ID>` to create and switch to a new branch containing only the v1 commit, using its hash.

<img width="732" alt="Screen Shot 2023-09-23 at 8 39 44 AM" src="https://github.com/belindadunu/deployment3.1/assets/139175163/8a5b6d6f-6f16-480c-92a4-d2276ebee0e6">

This allowed me to deploy the known good v1 code again.

To save these changes, we ran the following:

    - `$ git add .`

    - `git commit -m "Made changes based on rollback-v1"`
    
    - `git push -u origin main`

<img width="732" alt="Screen Shot 2023-09-23 at 8 37 27 AM" src="https://github.com/belindadunu/deployment3.1/assets/139175163/13086217-7dac-4e31-8605-ca21aa2acd28">

**Fully resolved?** Yes, successfully rolled back to proven version 1.

<img width="1435" alt="Screen Shot 2023-09-22 at 3 50 05 PM" src="https://github.com/belindadunu/deployment3.1/assets/139175163/2766fbe7-de8d-4496-8983-fcae33076384">

**Prevention:** For this situation, we tightened permissions so code must be reviewed before deployment. Junior engineers need senior approval; this prevents faulty code from being merged into the main.

## Next Steps

We need to improve any of our future deployment processes to prevent direct commits to the main branch. Other possible ways:

    - Require pull requests and approvals instead of direct commit
    
    - Lockdown version so any new version upgrades won't impact us unless we manually change it ourselves
    
    - Add staging environment for pre-production testing, if not already enabled
    
    - By adding checks and testing, we can prevent production outages caused by new code
    
    - Use tools like DataDog to monitor our systems and alert us immediately of any outages

## Post-Rollback Troubleshooting

While rolling back to the previous version resolved the immediate outage, we wanted to investigate the root cause of the failure in version 2.

After rolling back, we downloaded the Elastic Beanstalk logs from the failed deployment. In the logs, we noticed an error in application.py on line 42 while trying to parse the JSON data:

    - `urls = json.loads(data)`

This was causing a JSON decode error because `json.loads()` expects a string, but we were passing a file object.

Looking at the working version 1 code, we saw it was using:

    - `urls = json.load(data)`

Which correctly parses the JSON file object.

So the issue was version 2 introduced an error by using the wrong JSON parsing method for our data. Rolling back restored the correct code.

Documenting these kinds of findings is important for preventing future errors and noting these fixes helps strengthen the codebase.

## Conclusion
-----------------------------------------
While this incident only caused 10 minutes of downtime, it used up a significant portion of our allowed SLA downtime with Nike.

Our SLA allows only 20 minutes of total downtime per year. So with this 10-minute outage, we have now used up 50% of our allowed annual downtime in one incident.
