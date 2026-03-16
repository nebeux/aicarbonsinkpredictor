# Hi there!
This is a bit after the hackathon submission, but I decided to make a README anyway for those who are just looking around my profile/hackathon submissions.

This hackathon submission was really inspired by hardworking scientists. 
We wanted to make things easier for scientists who have been actively working for years to address climate change. 
Climate change will take many years to resolve, and this tool is meant to be a proof-of-concept showing that scientists can use the ocean to accelerate its resolution.

# What does each file/folder do? 
## requirements.txt
This file lists the libraries required for the project in case you plan to run it on your machine.

## model (folder)
### carbon_sink_model.pkl
This was the model we used to generate our carbon sink value. 

## carbon_sink_20k.csv
This was the training data used to train our model. Feel free to take a look through the 20k lines of simulated data we had 😂

## static (folder)
### style.css
This was our CSS for our HTML file. Basically, the file makes the frontend seem lively.

### app.js
This was our JS portion for our HTML file. What this did was initialize the map, send coordinates to the backend, receive data from the backend, and display it on the website!

## templates (folder)
### index.html
This was our HTML file. This contained the structure for our frontend, nothing much to say here :D

## unneededig (folder)
### training-data-generator.py
This was our Python file for generating **carbon_sink_20k.csv**. It uses a specific algorithm to train the data (with some randomness added) so the model is realistic and accurate. We desperately needed this file because real-world data was locked behind too many paywalls.

## app.py
Finally, the main part of our application, the backend, is the one and only **app.py**. What this did was fetch 5 ocean details using the coordinates from the frontend and APIs, feed them into our model, and have the model return a result, which we sent directly back to the frontend :D.

# Frameworks Used
We used the Flask framework as it was easy to work with and everyone knew how to code in Flask. 

# Final Note
We really hope you like our project, and we think it has real-world application when used correctly. It can also be used educationally as a tool to see where carbon sink rates are the highest!

made with love by Krish (nebeux), Sumeet (sumeetcubing), and Adhitya (coder175) ❤️
