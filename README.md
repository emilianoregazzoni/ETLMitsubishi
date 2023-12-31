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

