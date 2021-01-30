# habit@
**habit@** is a web app drawing inspiration from popular apps such as Instagram and Snapchat to create a supportive community where users can build habits together. 

Users create a schedule for when they plan to practice their new habits and post photos on the scheduled check-in dates as proof for following through with their goals. Users can follow one another and interact with eachother's posts via liking and commenting as a social media app. Users are also incentivized to continuously work on their habits as consecutive successful check-ins allow users to build up streaks to show off their consistency in habit building! Occasionally in life things do come up, so in order to allow for some forgiveness a missed check-in won't break a user's streak as long as they never miss 2 check-ins in a row. As they say, sometimes you just need a little nudge to get your feet to the gym and then chances are you'll work out before you decide to head back home. 

Let's make this year your year! Happy Habit Building!

# Setup
In your terminal navigate to the directory where you would like to clone the project and run the following:
```
git clone https://github.com/wolfhound115/habit-app.git
```

Navigate into the project folder and initiate a virtual environment to install dependencies and then run the following:
```
pip install -r requirements.txt
```

# How To Use
## Run Project
Navigate into the src folder and run the following:
```
python manage.py runserver
```

## Login
View the site at:
```
http://127.0.0.1:8000/habit/
```

The following usernames are accounts pre-populated with simulated data (the password for each account is: "dummypassword")
```
- eshwar (superuser admin account which can also access http://127.0.0.1:8000/admin to view the database)
- erik
- OctavioTheBest
- ellyphant
- jacorncob
- jojams
- thejustin
- win_ngo1
```

![Newsfeed](README_IMAGES/Newsfeed.png?raw=true "Optional Title")

## Features
### Starting a New Habit
##### Setting up a schedule for a new habit that the user would like to work on.

![New Habit Track](README_IMAGES/Create_Track_1.png?raw=true "New Habit Track")
![New Habit Track](README_IMAGES/Create_Track_2.png?raw=true "New Habit Track")
 

### Posting Habit Check-In
##### Creating posts on the scheduled days as proof of practicing the intended habits.

![New Habit Post](README_IMAGES/Check_in_Post.png?raw=true "Making Check-In Post")

### User Social Engagement
##### Other users can be found via searching for their name or username.

![Search Users](README_IMAGES/Search_Users.png?raw=true "Search Users")

##### Users can comment on eachother's posts as well as like posts and comments.

![Post Details](README_IMAGES/Post_Details.png?raw=true "Post_Details")


### User Profile
##### Visiting a user's profile can let you see all of the posts the user has made in their various habit tracks.

![Profile Posts](README_IMAGES/Profile_Posts.png?raw=true "Profile Posts")

##### You can also see all of the habit tracks a user is working on.

![Profile Tracks](README_IMAGES/Profile_Tracks.png?raw=true "Profile Tracks")

##### Details can also be viewed for specific tracks including current/best streaks and the number of posts made/missed/and to be expected for the habit.

![Track Details](README_IMAGES/Track_Details.png?raw=true "Track Details")



# Built With
- [Django](https://docs.djangoproject.com/en/3.1/) - The python web framework used
- [SQLite](https://www.sqlite.org/index.html) - The database used
- [Django-Recurrence](https://github.com/django-recurrence/django-recurrence) - Package used for creating patterns of recurring events

# Contributing
Currently this is an independent project so please contact the author for any details regarding pull requests

# Authors
Eshwar Manoharan 
