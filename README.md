# Improving the Reliability of Our URL Shortener 

Welcome back! In our [last deployment](https://github.com/belindadunu/jenkins-eb-deploy), we created a Jenkins pipeline to automatically build, test and deploy our URL shortener application from GitHub to Elastic Beanstalk. We also created a GitHub webhook to trigger this pipeline on code changes.

Now that we have a working deployment application, we want to improve reliability as we offer it as a service.

## The Story
-----------------------------------------
We are a tech start-up with a URL shortener service. We have a service level agreement (SLA) with Nike to provide access to our tool.

An SLA is like a customer service guarantee for services. For example, just like a restaurant promises to bring your food within a certain time, we promise a certain uptime and reliability.

Our SLA with Nike allows only 20 minutes of downtime per year. If anything happens, we must communicate the incidents to Nike.
 
## Incident Scenario
-----------------------------------------
A new hire deployed version 2 of the app by committing directly to the main branch. This triggered an automatic deploy that replaced version 1 in production.

The site then went down for 5 minutes, triggering an email alert. 

## Post-Incident Report
-----------------------------------------
**Reason for the incident:** An auto deploy of faulty version 2 code.

**Duration:** 5 minutes.

**Resolution steps:** Checked monitoring, logs, and git to identify the recent deployment. 

To roll back, I first ran `git log --oneline` to view recent commits. I saw version 2 had been merged into the main branch.

<img width="908" alt="Screen Shot 2023-09-22 at 11 05 09 AM" src="https://github.com/belindadunu/deployment3.1/assets/139175163/c12efce9-e28d-4aa8-93e7-78fe24c55b5c">

I initially thought of troubleshooting but that would take an unknown amount of time to figure out the root cause. I decided to complete a rollback.

To rollback, I could have checked out the main branch again, but that would still contain the faulty v2 code.

Instead, I wanted to rollback specifically to the last known good commit of version 1. I checked the hash of the v1 commit I wanted to revert to.

I then ran `git checkout -b <branch name> <commit hash ID>` to create and switch to a new branch containing only the v1 commit, using its hash.

This allowed me to deploy the known good v1 code again.

To save these changes, I ran the following:
    - `$ git add .`

    - `git commit -m "Made changes based on rollback-v1"`
    
    - `git push -u origin main`

<img width="735" alt="Screen Shot 2023-09-22 at 12 16 34 PM" src="https://github.com/belindadunu/deployment3.1/assets/139175163/65bf8b49-5ee3-42f7-a06c-41ac3e47259e">

<img width="905" alt="Screen Shot 2023-09-22 at 11 31 54 AM" src="https://github.com/belindadunu/deployment3.1/assets/139175163/5c98e485-fc0f-4978-8598-c2c418757f72">

**Fully resolved?** Yes, successfully rolled back to proven version 1.

**Prevention:** For this situation, I tightened permissions so code must be reviewed before deployment. Junior engineers need senior approval; this prevents faulty code from being merged into the main.

## Next Steps
-----------------------------------------
We need to improve any of our future deployment processes to prevent direct commits to the main branch. Other possible ways:

    - Require pull requests and approvals instead of direct commit
    
    - Add staging environment for pre-production testing, if not already enabled
    
    - By adding checks and testing, we can prevent production outages caused by new code
    
    - Use tools like DataDog to monitor our systems and alert us immediately of any outages

## Conclusion
-----------------------------------------
While this incident only caused 5 minutes of downtime, it used up a significant portion of our allowed SLA downtime with Nike.

Our SLA allows only 20 minutes of total downtime per year. So with this 5-minute outage, we have now used up 25% of our allowed annual downtime in one incident.
