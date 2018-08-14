
from sqlalchemy import func
from model import User, Student, Behavior, Intervention, Progress, app
import random
from datetime import datetime
from faker import Faker
from model import connect_to_db, db


def load_users():
    """load fake users into the database"""

    fake = Faker()

    for user in range(25):
        user_name = fake.name()
        password = fake.password(length=10, special_chars=False, digits=False, upper_case=True, lower_case=True)
        user = User(user_name=user_name, password=password)
        db.session.add(user)

    db.session.commit()


def load_students():
    """load fake students into the database"""

    fake = Faker()

    for student in range(500):
        fname = fake.first_name()
        lname = fake.last_name()
        birthdate = fake.date_of_birth(tzinfo=None, minimum_age=5, maximum_age=18)
        user_id = random.randint(1, 20)
        # phone_number = fake.phone_number()
        # photo = still figuring this out.
        student = Student(fname=fname, lname=lname, birthdate=birthdate, user_id=user_id)
        db.session.add(student)

    db.session.commit()


def load_behaviors():
    """load behaviors from u.behavior into database"""

    b_dict = {'Agressive-Bullying': {'Description': ['Verbally or physically harass others', 'causing them to report incidents to adult', 'Engage in bullying activity', 'intimidation, threats', 'Be observed hitting, kicking, and repeatedly pushing others', 'Demonstrate Intense anger,Frequently lose temper or have blow-ups', 'Become easily frustrated, Instigate and be involved in frequent conflicts, arguments, and fights', 'Value being seen as tough and one to be feared or avoided', 'Demonstrate threatening body language, like puffing up chest, clenching fists, and flinching at others'], "Appropriate Interventions": ['Move to a new location in the classroom', 'Take away privileges', 'Take away unstructured or free time', 'Talk one on one with student']},
        'Anxiety': {'Description': ['Unable to control their constant worries', 'Frequently ask how to do tasks', 'Apprehensive to start and work on own', 'Give up and discontinue effort easily', 'Unable to relax', 'Seem shy and not seek out help', 'volunteer, or participate'], "Appropriate Interventions": ['Alternative modes of completing assignments', 'Break down assignment', 'Draw a picture or write in a journal', 'Encourage interaction with a more self confident student', 'Listen to music', 'Reassurance', 'Reduce assignment', 'Take a break', 'Teach coping skills', 'Teach relaxation techniques', 'Teach social skills']},
        'Confrontational/Defensive': {'Description': ['Lash out verbally at others', 'Challenge the authority of the adult', 'Project blame onto others', 'Unable to admit a mistake', 'Have a strong sense of injustice and being wronged', 'Easily provoked, irritate, and upset'], "Appropriate Interventions": ['Avoid power struggles', 'Explain assignment', 'Logical consequence', 'Take a break', 'Teach conflict resolution skills', 'Teach relaxation techniques', 'Use calm neutral tone']},
          'Defiant': {'Description': ['Engage others in arguments and conflict', 'Dislike being told what to do', 'Smile, cross arms, stomp feet, etc when reusing to follow directives', 'Only do tasks or activities they like or enjoy', 'Quietly refuse to do as told', 'Prefers to focus with intensity on one task'], "Appropriate Interventions": ['Acknowledging positive behavior', 'Clear and concise directions', 'Clear, consistent, and predictable consequences', 'Give choices', 'More structured routine', 'Simple Reward Systems, & Incentives', 'Use calm neutral tone']},
          'Disorganized': {'Description': ['Frequently turn in assignments late', 'Forgetful', 'Easily lose things', 'Difficulty staying on task', 'Bring wrong materials to class', 'Complete work and not turn it in'], "Appropriate Interventions": ['Break down assignment', 'Color coded folders', 'Organize materials daily', 'Pause before giving a direction', 'Turn desk around', 'Visual schedule']},
          'Disrespectful': {'Description': ['Frequent engagement of confrontation', 'Frequent talking back to adults', 'Negative facial expressions', 'Lack of common courtesy', 'Poor attitude', 'Unwilling to consider other ideas and opinions', 'Take and use things without asking or caring about personal space'], "Appropriate Interventions": ['Acknowledging positive behavior', 'Reflection sheet', 'Teach social skills', 'Use calm neutral tone']},
          'Disruptive': {'Description': ['Speak out of turn', 'blurt out', 'Try to engage others while they are working', 'Drop things, laugh, or makes noises on purpose', 'Out of seat, walking around class, getting drinks, sharpening pencil, etc', 'Bother other students'], "Appropriate Interventions": ['Ignore', 'Praise when on task', 'Redirection', 'Avoid power struggles']},
          'Failing to turn in work': {'Description': ['Have low academic ability', 'Have a very messy locker, desk, or backpack', 'Have an unstable home and little parental follow through', 'Not know the directions or the content', 'Be disorganized', 'Have a hard time getting started'], "Appropriate Interventions":  ['Daily planner', 'Color coded folders', 'More structured routine', 'Organize materials daily', 'Provide a container for the student’s belongings', 'Teach organizational skills']},
          'Frustration': {'Description': ['Refuse and snap at offers for help', 'Blame others or things for problems', 'Perseverate on a topic, problem, or issue', 'Quick to react with anger', 'Lash out verbally and physically'], "Appropriate Interventions": ['Break down assignment', 'Clear and concise directions', 'Give choices', 'Reflective listening', 'Stress ball or fidget', 'Take a break', 'Use calm neutral tone']},
          'Hyperactivity': {'Description': ['Be fidgety with hands or feet and squirm or reposition constantly in seat', 'Often leaves seat in classroom or in other situations in which remaining seated is expected', 'Often on the go or often acts as if driven by a motor', 'Often talks excessively', 'Need and seek attention from everyone', 'Have difficulty finishing thoughts and tasks', 'Be forgetful'], "Appropriate Interventions": ['Have student repeat directions back', 'Headphones', 'Individual work space', 'More structured routine', 'Non verbal cues', 'Send student on errand', 'Stress ball or fidget', 'Use timer', 'Stand while working']},
          'Impulsive': {'Description': ['Interrupt others', 'Have trouble waiting turn and sharing', 'Start working before told to or before directions are given', 'Act without considering the consequences', 'Fidgety', 'Have trouble waiting in line and transitioning'], "Appropriate Interventions": ['Alternative modes of completing assignments', 'Daily planner', 'Have student repeat directions back', 'More structured routine', 'Redirection', 'Stress ball or fidget', 'Take a break']},
          'Inappropriate language': {'Description': ['Swear or curse', 'Make inappropriate innuendoes', 'Repeat others in a deliberate and patronizing way', 'Use sensitive words in an insulting or joking manner', 'Use racial, stereotypical, or culturally insensitive words'], "Appropriate Interventions": ['Avoid power struggles', 'Clear, consistent, and predictable consequences', 'Reflection sheet', 'Speak in calm and neutral tone', 'Take away privileges']},
          'Lack of participation': {'Description': ['Appear withdrawn or shy', 'Look down', 'Fall behind academically', 'Have a poor sense of self', 'Appear sad or unhappy', 'Have an “I don’t care attitude', 'Be distressed, upset, or preoccupied', 'Frequently say “I don’t know'], "Appropriate Interventions": ['Non verbal cues', 'Praise when good attitude and involvement occur', 'Teach relaxation techniques', 'Teach social skills']},
          'Lack of responsibility': {'Description': ['Fail to return work', 'Never make up missed work', 'Have poor attendance and punctuality', 'Come to class unprepared', 'Have incomplete assignments', 'Make many excuses'], "Appropriate Interventions": ['Assign a classroom job', 'Clear, consistent, and predictable consequences, Rewards', 'Simple Reward Systems, & Incentives', 'Teach organizational skills']},
          'Lack of social skills': {'Description': ['Seem to interact and navigate environment in an awkward, weird, or odd manner', 'Tease others frequently', 'Seem emotionally immature', 'Class clown', 'Poor interactions with others', 'Be overly animated, dramatic, or sensational'], "Appropriate Interventions": ['Assign a buddy or partner', 'Draw a picture or write in a journal', 'Non verbal cues', 'send student on errand', 'Teach relationship skills']},
          'Low or no work completion': {'Description': ['Have low academic ability', 'Be sad or depressed', 'Become frequently frustrated and discouraged with work', 'Have poor organizational skills', 'Dislike school', 'Have trouble focusing and attending'], "Appropriate Interventions": ['Break down directions', 'Clear, consistent, and predictable consequences', 'Daily planner', 'Give choices', 'Help student start assignment', 'Praise student frequently', 'Reduce assignment']},
          'Lying/Cheating': {'Description': ['Appear suspicious, tense, nervous, uptight, etc', 'Tattle often', 'Have difficulty taking responsibility', 'What they are saying doesn’t quite add up'], "Appropriate Interventions": ['Logical consequence', 'Reflection sheet', 'Take away privileges', 'Use calm neutral tone']},
          'Name calling': {'Description': ['Say inappropriate words, swear, demean, tease, etc', 'Repeat others in a deliberate and patronizing way', 'Have other students frequently complain about them'], "Appropriate Interventions": ['Reflection sheet', 'Speak in calm and neutral tone', 'Take away privileges', 'Teach relationship skills']},
          'Negative attitude': {'Description': ['Make self defeating comments', 'Minimize the successes of others', 'Be dismissive', 'Always find fault in everything', 'Say they don’t care, don’t want to do something, or hate things'], "Appropriate Interventions": ['Engage student', 'Praise when good attitude and involvement occur', 'Rewards', 'Simple Reward Systems, & Incentives', 'Teach coping skills']},
          'Off task/Disruptive': {'Description': ['Annoying and distracting to others', 'Get out of seat frequently', 'Failing to transition appropriately', 'Yell out', 'Bother other students'], "Appropriate Interventions": ['Clear, consistent, and predictable consequences', 'Explain directions', 'Ignore', 'More structured routine', 'Praise when cooperative and well behaved', 'Redirection', 'Turn desk around']},
          'Off task/Non-disruptive': {'Description': ['Quietly blend in while doing nothing, doodling, or appearing to work', 'Day dream, look out window, around the room, look past the teacher, at other students, stare, etc', 'Draw or do other tactile activities while lesson is being presented'], "Appropriate Interventions": ['Explain assignment', 'Have student repeat directions back', 'More structured routine', 'Use timer']},
          'Poor coping skills': {'Description': ['Highly reactive and sensitive', 'Have difficulty taking praise or criticism', 'Often blame others', 'Seem frequently and easily overwhelmed and overloaded', 'Unable to express feelings', 'Become frustrated easily'], "Appropriate Interventions": ['Draw a picture or write in a journal', 'Listen to music', 'Non verbal cues', 'Proximity to students', 'Take a break', 'Teach social skills']},
          'Poor peer relationships': {'Description': ['Frequent conflicts with peers', 'Annoy and irritate others', 'Eat lunch alone or play alone on playground', 'Trouble getting along in groups or pair work', 'Frequently argue or fight with others'], "Appropriate Interventions": ['Proximity to students', 'Talk one on one with student', 'Teach social skills']},
          'Poor self esteem': {'Description': ['Be self defeating', 'Hesitant to try new things or challenging tasks', 'Easily cease effort', 'Never feel they are good enough', 'Be a perfectionist', 'Take on more than they can handle'], "Appropriate Interventions": ['Alternative modes of completing assignments', 'Draw a picture or write in a journal', 'Give choices', 'Praise student frequently', 'Teach relaxation techniques']},
          'Rushing through work': {'Description': ['Often be the first to turn in assignments, tests, or put their pencil down', 'Have answers that make no sense', 'Poor quality work', 'Eager to play, socialize, or do other things'], "Appropriate Interventions": ['Break down assignment', 'Have student take frequent breaks, do errand, or active job', 'More structured routine', 'Use timer']},
          'Sadness/Depression': {'Description': ['Have persistent sad, anxious, or “empty” feelings', 'Show a loss of interest in activities or hobbies once pleasurable', 'Withdraw from friends and peer group', 'Slumping and diminishing grades, missing work, failing tests/quizes', 'Overeat or have a loss of appetite'], "Appropriate Interventions": ['Draw a picture or write in a journal', 'Explain directions', 'Frequent home contact', 'Listen to music', 'Praise student frequently']},
          'Somatic complaints':{'Description': ['Have frequent complaints of body aches (head, stomach, extremities) that have not been shown to have physiological origins', 'Ask to go home due to not feeling well', 'Seem needy and overly reliant on others'], "Appropriate Interventions": ['Give choices', 'Reassurance', 'Reflection sheet', 'Take a break', 'Use timer']},
          'Stealing': {'Description': ['Be unable to explain how and where they got something from', 'Brag to others of new items'], "Appropriate Interventions": ['Clear, consistent, and predictable consequences', 'Office referral', 'Take away privileges', 'Use calm neutral tone']},
          'Tantrums/Out of control': {'Description': ['Fail to respond to any redirection, calming, deescalation, etc', 'Run from adults and authority figures', 'Unable to deescalate after reasonable period', 'Smile and taunt others while threatening', 'Express no concern for consequences'], "Appropriate Interventions": ['Avoid power struggles', 'Clear and concise directions', 'Clear, consistent, and predictable consequences', 'Give choices', 'Ignore', 'Reduce assignment', 'Stress ball or fidget', 'Use calm neutral tone']},
          'Tardiness': {'Description': ['Frequently come to school late', 'Over socializing in between periods', 'Have trouble navigating the halls and school', 'Be disorganized', 'Be easily distracted'], "Appropriate Interventions": ['Acknowledging positive behavior', 'Clear, consistent, and predictable consequences', 'Daily planner', 'More structured routine', 'Rewards, Simple Reward Systems, & Incentives', 'Visual schedule']},
          'Unable to work independently': {'Description': ['Frequently ask teacher or other students for help and assistance, or to do items for them', 'Always need to be around others to work', 'Have difficulty completing assignments', 'Quick to cease effort wen task becomes challenging', 'Makes up many excuses', 'Act helpless'], "Appropriate Interventions": ['Break down directions', 'Break, moving position in class', 'Clear, consistent, and predictable consequences', 'Organize materials daily', 'Reduce assignment', 'Use timer']},
          'Unmotivated': {'Description': ['Seem lackluster, sluggish, emotionally flat', 'Express no concern about incomplete work, grades, achievement', 'Not appear to enjoy school', 'Have frequent absences or frequent reports of illness'], "Appropriate Interventions": ['Break down directions', 'Draw a picture or write in a journal', 'Engage student', 'Give choices', 'Praise when good attitude and involvement occur', 'Reflection sheet']}}

    #Breaks up dicitionary into required Class attributes + instantiates a Behavior object
    for behavior_name in b_dict:
        behavior_description = b_dict[behavior_name]['Description']
        behavior = Behavior(behavior_name=behavior_name,
                            behavior_description=behavior_description)
        db.session.add(behavior)

        #instantiates an intervention object and appends to the appropriate behavior object.
        for i_name in b_dict[behavior_name]['Appropriate Interventions']:
            #check if intervention with that intervention name is in the db ,if not, create it and add it to the behavior.
            #if it is, get that intervention and add it to the behavior and the behavior to the intervention.
            if Intervention.query.filter(Intervention.intervention_name==i_name).first():
                x = Intervention.query.filter(Intervention.intervention_name==i_name).first()
                x.behaviors.append(behavior)
                behavior.interventions.append(x)
            else:
                intervention = Intervention(intervention_name=i_name)
                db.session.add(intervention)
                intervention.behaviors.append(behavior)
                behavior.interventions.append(intervention)

    db.session.commit()


def load_progress():
    """load progress from u.progress into database"""

    fake = Faker()

    #generates random comment from list
    comments = ["great progress", "no progress yet", "still happens, but not as much as initially",
                "friend was moved to other class, behavior improved", "snickers bribe helps!"]

    #generates random student_id
    all_students = db.session.query(Student.student_id).all()

    #generates random behavior_id
    all_behaviors = db.session.query(Behavior.behavior_id).all()

    #generates random intervention_id
    all_interventions = db.session.query(Intervention.intervention_id).all()

    #generates random user_id
    all_users = db.session.query(User.user_id).all()

    for progress in range(5000):
        student_id = random.choice(all_students)
        behavior_id = random.choice(all_behaviors)
        intervention_id = random.choice(all_interventions)
        date = fake.past_date(start_date="-360d", tzinfo=None)
        user_id = random.choice(all_users)
        rating = random.randint(0, 10)
        comment = random.choice(comments)

        progress = Progress(student_id=student_id, behavior_id=behavior_id,
                            intervention_id=intervention_id, date=date,
                            user_id=user_id, rating=rating, comment=comment)

        db.session.add(progress)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_users()
    load_students()
    load_behaviors()
    load_progress()
