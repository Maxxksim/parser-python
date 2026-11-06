PYTHON 3.13 MySQL 8.4 Redis 8.8

Steps to start the project:

Clone the project to yourself  
Copy .env.example to .env in root directory  
Change environment variables if you want your settings of the parser:        
Before start parsing you must configure your proxy:  
Replace proxies on yours in array of proxies which is proxy config      
You can find the config in the next path: config/proxy_config.py and  
than fill PROXY_USERNAME, PROXY_PASSWORD  

LOG_MODE = set file if you want to get logs to Logs/logs.log otherwise set debug to get log to STDOUT  
NUMBER_PROCESSES = set the number of processes which will parse otherwise only one process will do it  

Open a terminal in root directory  

For Windows system via Docker:     
Start docker if you didn't it before  

1. Set DB_HOST in db in your .env file    
2. Set REDIS_HOST in redis in your .env file    
Then enter the commands in the terminal:  
3. docker compose up db redis -d  
4. docker compose run --rm migrate  
5. docker compose run --rm start-parser    

For Unix systems:  

Enter the commands in the terminal:    
1. python3 -m venv .venv     
2. source .venv/bin/activate  
3. pip install -r requirements.txt  
4. docker compose up db redis -d      
5. python3 migrate.py     
6. python3 main.py      