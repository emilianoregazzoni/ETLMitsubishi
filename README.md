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




