# AWS-Lambda-Function-NBA-Webscraper 
MIDS - 706 Final Project NBA webscraper

[![](http://img.youtube.com/vi/8DBP9GBSGg0/0.jpg)](http://www.youtube.com/watch?v=8DBP9GBSGg0 "Final Project ")

## Project Summary

This project demos how to create a scalable serverless data engineering pipeline, using an Amazon Lambda function. This pipeline is designed for webscraping, but  the concepts shown can easily be extended to other tasks that involve scheduled webscrapes or the use of the Event Bridges in general. 

The serverless lambda function runs code that scrapes basketball reference (https://www.basketball-reference.com/leagues/NBA_2017_totals.html) to pull NBA totals for a specified season in order to easily analyze and manipulate the data. The lambda function is ran in Cloud 9, and once deployed can be ran and tested in the console's Lambda Function designation. After which I created the Event Bridge that Triggers the lambda function to run at the end of every day (but for the sake of this demonstration I made it run for 5 minutes). You can check the status of your Event Bridge by clicking the monitoring tab in the AWS Function Console. It tells you the success rate of your function:

https://github.com/dapoade/Data-Engineering-Project/blob/main/Cloud%20Watch%20Metrics.png

In most of the examples I've seen, an S3 bucket is changed, added, or deleted, resulting in a trigger for the lambda function. My project takes a slightly different approach by manually creating the trigger using Event Bridge (Cloud Watch Events). I also tested requests for every minute, three minutes 5 minutes and every hour. 

<img width="801" alt="Add Trigger 1" src="https://user-images.githubusercontent.com/69828169/100197309-268c5500-2ec8-11eb-9fc1-5da704714ce8.png">


<img width="472" alt="Add Trigger 2" src="https://user-images.githubusercontent.com/69828169/100197369-3c9a1580-2ec8-11eb-8d25-1e347833605e.png">




So it appears as if my pipeline can handle a number of requests; the only caveat would be whether or not basketball reference chooses to block my api address for repeated attempts at scraping their website. The resulting output makes it such that the called table is now put into an S3 bucket with a in the form of a csv which allows for editing of documents. In addition to scraping NBA data this, drew parallels between this and when I worked in IT consulting and had to run status reports on newly acquired data. I think having access to something such as this would make life easier through automation. 







