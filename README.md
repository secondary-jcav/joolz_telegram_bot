**UPDATE**   
This is a few years old. Rotten Tomatoes no longer offers a free API
So, will change this. In the meantime, The Movie Database free API seems to work ok

**Everything below this is deprecated**    

**Goals**  
1)Create a personalized bot using Telegram's python API    
2)Run it on AWS EC2 instance or lambda


**Requirements**  
- Run pip install -r requirements.txt to get the needed python packages 


**Execution**  
 In echobot.py, copy bot token in the updater call that runs in main()
- Change start() & help () as needed.
- Logic for the desired actions go in echo

**Current Capabilities**   
After being given a movie title, bot checks that movie's Rotten Tomatoes
score and returns that to the user.



