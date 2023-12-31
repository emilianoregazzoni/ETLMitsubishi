# ETLMitsubishi :car: :japan:
## __ETL job transformation using Airflow, TaskFlow API, Python, twelvedata API, Docker and PostgreSQL__ 

In this project I worked with information about Mitsubishi shares. The goal here was to develop an ETL job using Airflow, Python and other tools. The basic Extract, Transform and Load process is represented here.

## 1. Googling and research about the API.

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




## 2. Python, Airflow, Docker, PostgreSQL and TaskFlow API 

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

### 2.2 Python

Then I decided to use the Taskflow API to work with in Airflow.
Taskflow allows the users to write Python code rather than Airflow code, it is more legible and easy to understand than Airflow code.
Airflow 2.0 provides a decorator called @task that internally transforms any Python function into a PythonOperator. 
One of the most important things using @task is that you can finally pass data from one task to another without having to write any XComs logic.
When I added the decorator @task, Airflow knows that the functions are tasks and it should be treated as ones.
I found this awesome article from Anna Geller (Thanks a lot Anna!) which helped me a lot to understand this new approach from Airflow 2.0:
https://towardsdatascience.com/taskflow-api-in-apache-airflow-2-0-should-you-use-it-d6cc4913c24c

Then I created three @tasks which represent the whole process (Extract, Transform and Load)

```
# define ETL job
def ETLMitsubishi():

    # EXTRACT: Query the info from twelvedata, the endpoint /price which says the price of a share right now
    @task()
    def extract():

        info = {'symbol': 'MSBHF', 'apikey': '*** YOUR API KEY ***'}
        r = requests.get("http://api.twelvedata.com/price?", params=info)

        # Get the json
        r_string = r.json()
        print(r_string)
        return r_string
```
Here I made the request to the API from twelvedata and convert into JSON, then the function return it.

Then I created a function to transform the data, the main transformation here is to take the price of a share and add the datetime the request was made. Then the function return a dictionary.

```
 # TRANSFORM: Transform the API response, date and time added to load to database
    @task()
    def transform(mitsubishi_json: json):

        mitsubishi_str = json.dumps(mitsubishi_json)
        transformed_str = transform_Mitsubishi(mitsubishi_str)

        # turn string into dictionary
        ex_dict = json.loads(transformed_str)
        print(ex_dict)
        return ex_dict   
```

The third function is used to load the dictionary created and store the data into the database.

```
# Save the data into Postgres database
    @task()
    def load(mitsubishi_data: dict):

        try:
            connection = psycopg2.connect(user="airflow",
                                        password="airflow",
                                        host="postgres",
                                        port="5432",
                                        database="mitsubishi")
            cursor = connection.cursor()
            postgres_insert_query = """INSERT INTO mitsubishi_info (price, timestamp) VALUES ( %s, %s );"""
            print(postgres_insert_query)

            record_to_insert = (mitsubishi_data[0]["price"],mitsubishi_data[0]["timestamp"] ) # let , so python can understand is a record with 1 column
            
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully")

        except (Exception, psycopg2.Error) as error:
            
            print("Failed to insert record into tableeee", error)
            
            if connection:
                cursor.close()
                connection.close()
                print("Connection is closed")
            
            raise Exception(error)
        finally:
            # close db
            if connection:
                cursor.close()
                connection.close()
                print("Connection is closed")  
```

Finally the flow was this:

```
    # Defining the flow in Airflow
    mitsubishi_data = extract()
    mitsubishi_summary = transform(mitsubishi_data)
    load(mitsubishi_summary)

# call the DAG
mitsubishi_dag_posgres = ETLMitsubishi() 
```
I created a variable called mitsubishi_data which had the information I got from function extract (price of the share). Then the variable mitsubishi_summary had the information transformed and it returned a dictionary. Finally I called the load function to save the dictionary into the database.

I tried some times the DAG manually:
![image](https://github.com/emilianoregazzoni/ETLMitsubishi/assets/20979227/76adf757-d37b-43f6-8457-f82d2c04f1da)

Then in Airflow it looked like this:

![image](https://github.com/emilianoregazzoni/ETLMitsubishi/assets/20979227/f51a8be4-e4a9-46e8-aa47-076a96225301)

All the executions were successfully.

Then I checked the logs, the best way to see if it is everything ok in the back, for example extract log:

![image](https://github.com/emilianoregazzoni/ETLMitsubishi/assets/20979227/8ca21096-d4b4-4ccd-aa9e-bcf957224d6b)

It shows exactly the information I requested on the API call.

Then I checked the transform log:

![image](https://github.com/emilianoregazzoni/ETLMitsubishi/assets/20979227/04dc2af0-55f9-48d1-a4ba-3731be4a51e5)

Here I observed the transformation I made, add the time and hour to the value of the share, then returned the dictionary.

After that I checked the info was stored perfectly.

![image](https://github.com/emilianoregazzoni/ETLMitsubishi/assets/20979227/cde4c99e-71fa-4f8d-815b-4a62f818178c)

Finally I checked the database:

![image](https://github.com/emilianoregazzoni/ETLMitsubishi/assets/20979227/00faf59e-ce0e-4f84-a982-c388f1b425b2)

The information is ok in the database too. I had the information available in PostgreSQL.

## 3. Conclusions 

This ETL transformation project using Python, Airflow, Docker, and various other technologies has been a highly productive and enriching experience for me.

Throughout this work, I have demonstrated the effectiveness of the chosen technologies for data transformation, automating processes with Airflow, and ensuring portability and scalability with Docker. However, this venture is merely the beginning, as the field of data engineering is infinitely expansive.
In summary, this work has not only been a test of my technical skills but also a reminder of the vast possibilities in data engineering. Curiosity and continuous learning are essential in this dynamically evolving field.

I would like to express gratitude to Andreas Kretz for his invaluable contribution and dedication to teaching to all data engineering enthusiast around the world. Some parts of my project took valuable ideas from his academy as an input, which not only provided a solid conceptual foundation but also inspired me to explore and apply those insights in a practical context.

