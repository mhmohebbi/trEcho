# trEcho
Track the delivery of your package using Amazon Alexa!

## Inspiration
Wouldn't it be great if you could track the delivery of any packages you order? And better yet, completely hands free? Look no further, trEcho is here for the rescue!

## What it does
trEcho enables you to track and keep track of any package you've ordered with Innovapost in real time using Amazon Alexa. This helps users gain the most accurate and up-to-date information about where their parcel might be, and in how long it will arrive. We also created an easy-to-use web app that the customer would be able to access to directly see where their package is.

## How I built it
We created a custom skill on Amazon Echo show to the predicted arrival time of a package a user ordered. To do this, we created an algorithm that would analyze Innovapost's database of current parcels being delivered. Then, using the Google Maps API, we calculated the most likely current position of the delivery vehicle based on the time since it last shared it's location. We wanted to make our algorithm as accurate as possible, so we put a lot of thought into calculating the precise distances travelled by the delivery vehicles. This meant we investigated the Google Maps API thoroughly, as well as using latitude and longitude calculations to be as accurate as possible.

## Challenges I ran into
We ran into a lot of challenges trying to create a custom skill for the Amazon Echo Show and connecting it with our database. In addition, we had to put a lot of thought into ensuring our longitude and latitude calculations were accurate.

## Accomplishments that I'm proud of
As Innovapost's servers can take in over 30 million requests during peak delivery season, we wanted to create a product that would lighten some of this demand. Therefore, we set up a cache in our system for fetching the parcel's location. In this way, we believe that we have found a successful compromise between providing the most accurate data and not overloading Innovapost's servers.

## What I learned
Neither of us has any prior experience with Amazon Alexa, so there was a lot of learning involved to learn how to use it and incorporate into our hack. We also learnt about trying to cater our product to consumers to maximize the ease and enjoyment of use. 

## What's next for trEcho
In the future, we hope to be able to utilize the screen on the Amazon Echo Show to be able show the predicted location of the delivery vehicle based on the Google Maps API. In addition, we're hoping to improve the accuracy as our algorithm, possibly using ML to improve the quality of the location predictions.
