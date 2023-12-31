# ETLMitsubishi
## __ETL job transformation using Airflow, TaskFlow API, Python, twelvedata API, Docker and PostgreSQL__ 

In this project I worked with information about Mitsubishi shares. The goal here was to develop an ETL job using Airflow, Python and other tools. The basic Extract, Transform and Load process is represented here.

## 1.Googling and research about the API to use.

First of all I needed a good finance API to get the information from shares. In this case I was interested on the price of Mitsubishi shares. I tried Google Finance API and API Layer but later I found a better place called twelvedata.com which offers a lot of endpoints to get information about real time price, forecasting and more.

![image](https://github.com/emilianoregazzoni/ETLMitsubishi/assets/20979227/f80400b3-857c-4589-bfc2-897c13cbec19)

Once I created an account, then I needed to create a token to use any endpoint later. It is really easy to do that, just a couple of clicks and then I had the token ready to use.

![image](https://github.com/emilianoregazzoni/ETLMitsubishi/assets/20979227/aa9aa753-8f3f-4ad2-ba6b-62a4d314e7c9)

In this case I used the endpoint /price , which gives you the price of any share listed on Nasdaq
After read how use the API I figured out that the endpoint /price expects at least 2 parameters:

- apikey: the token previously generated
- symbol: the symbol associated to the company

![image](https://github.com/emilianoregazzoni/ETLMitsubishi/assets/20979227/d76acb0d-c6f8-45d1-bb2f-2317ab6b3803)

In this case the symbol of Mitsubishi corporation is “MSBHF” then I added my token, and got the response from the API:

![image](https://github.com/emilianoregazzoni/ETLMitsubishi/assets/20979227/9fc1dce9-8895-4294-a8dc-d7f2ac82e7cb)

API returns the price of the share at the moment I requested.
I checked in the official Nasdaq site if it was ok:

![image](https://github.com/emilianoregazzoni/ETLMitsubishi/assets/20979227/5768848a-4b09-4f10-8b29-2e3a55bf881b)

The information is perfect, the API works fine, this is the only origin source of information the project has.




## 2.Python, Airflow, Docker, PostgreSQL and TaskFlow API 

My target here was to develop an easy ETL job but using interesting tools like Airflow, Python, Docker and more, so I just took the price of the share from the API and then I created a variable in Python which takes the date and time from the operating system. This was the information stored into database.

![image](https://github.com/emilianoregazzoni/ETLMitsubishi/assets/20979227/bf169c6b-5e71-4a70-a48c-0e5c85564b5e)


### 2.1 Docker and services

The file I used is a typical docker compose file which defines the structure I wanted for the project. You can find more resources about that here:

https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
https://airflow.apache.org/docs/docker-stack/build.html

Or you can search on the internet any docker compose file which gives you an instance for airflow, postgres and redis, you can use it too. This is for setup your environment.
In my case I took the file provided by the Andreas Kretz academy. 

_Thank you so so much Andreas if you read this someday!_

I will not enter in details about the docker compose file, but the logic here was to use an image from Airflow 2.2.4, then let the automatic dependencies and configurations by default.
Then in Service section it is configured the Postgres database with default ports, with a user to access called Airflow. Also the file contains the adminer configured to deal with the database Postgres.
Then it has the Redis and Celery also configurated required to deal with the tasks and the flow. Also it has the Airflow webserver configurated by default. 
Those are the services I used for the project, remember this is an Apache Airflow file pre-configurated with a lot of sections I did not change.
Once I had the file I executed the command: docker compose up. 
```
docker compose up
```

This command started up all the environment in Docker and and turned on all the services I had in the docker-compose.yml file

![image](https://github.com/emilianoregazzoni/ETLMitsubishi/assets/20979227/2c439239-5e05-44ba-8e3a-a0666e027ef8)

Then I saw in docker all the services running:

![image](https://github.com/emilianoregazzoni/ETLMitsubishi/assets/20979227/1d7b8d71-c198-4a35-ada5-c2b594566878)

After I checked by docker that all the services were running, it was time to actually check them.

Airflow was ok.

![image](https://github.com/emilianoregazzoni/ETLMitsubishi/assets/20979227/a1e0689f-a834-484c-859d-6f969bbd6fa5)

When I instantiated airflow I saw several examples that come by default to explore the tool

![image](https://github.com/emilianoregazzoni/ETLMitsubishi/assets/20979227/10246e9c-3b17-4b93-a13a-af8b5d2d2b48)

Then I checked PostgreSQL, also it was ok.

![image](https://github.com/emilianoregazzoni/ETLMitsubishi/assets/20979227/49aab837-86d1-4697-b4c9-e69a1648b406)


Once I figured out that PostgreSQL was ok, it was time to create the database which stores the information worked with.
I decided to create a simple database called “mitsubishi”, and one table called “mitsubishi_info”, like that:

![image](https://github.com/emilianoregazzoni/ETLMitsubishi/assets/20979227/49657eb0-5bab-4164-a7b7-40378339aca2)

“price” refers the value I get from twelvedata API and “timestamp” is a variable that I created on Python that refers to the time and hour I called the API.





