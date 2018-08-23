Summary:

Carrot Stix is an intervention tool aimed at teachers and parents to monitor targeted student behaviors with specific interventions and dynamically chart progress over time.  Users register and add students they would like to monitor.  They can then identify behaviors they would like to target and choose associated interventions.  Users can target multiple behaviors for each student and enter multiple progress reports to gauge the success of the intervention.  Student progress is dynamically charted to visualize progress and the intersection of multiple behaviors.  With the click of a button, users can text progress reports and comments to parents to facilitate collaboration between families and schools.

The app is written in Python with a Flask framework and uses SQLAlchemy to communicate with a postgres database.  I used the Twillio API to create a texting feature in my app, along with Faker and Random User Generator APIs to help generate test data that I could work with in development. 


Tech Stack:

Python, Flask, Jinja, SQLAlchemy, Javascript, Bootstrap, HTML, CSS, Twillio API, Random User Generator API, Faker API


Features:
![Alt text](~/Users/lauralhorton/src/behavior_project/static/images/homepage.jpg raw=true "carrot_homepage")

![Alt text](/Users/lauralhorton/src/behavior_project/static/images/user_page.png raw=true "carrot_homepage")

Users login on the homepage and are then able to view the students they have registered to thier accounts. From any place on the site, users can add a new student or search for an existing student.  

![Alt text](/Users/lauralhorton/src/behavior_project/static/images/user_page.png raw=true "carrot_homepage")

When they select a student, they can view a list of the monitored behaviors and a graph displaying the student's progress in that behavior.  Users can access progress reports for each of the data points on the graph directly below.  

![Alt text](/Users/lauralhorton/src/behavior_project/static/images/send_sms raw=true "carrot_homepage")

A user is able to see a graph of only one specific behavior by clicking on that behavior.  From that page, the user can text a progress report to the number registered with the student.

![Alt text](/Users/lauralhorton/src/behavior_project/static/images/add_progress.sms raw=true "carrot_homepage")

A user is also able to add new pogress reports for that student.  To ensure accurate evaluation, users are prompted to employ the same intervention for a specific behavior at least six times before switching to a new intervention. Research suggests using the same intervention for six to eight data points provides more meaningful evaluation and an opportunity to gauge progress.

Carrot's focus is on functionality and simplicity to maintain an efficient user experience.  Additional information about behaviors and associated interventions is hidden in modal windows that are easily accessible without distracting from navigability of the site.

Carrot was created by Laural Horton, a software engineer in Oakland, CA. In a previous life she taught high school special education, also in Oakland.  Learn more about the developer on [LinkedIn](https://www.linkedin.com/in/lauralhorton).
