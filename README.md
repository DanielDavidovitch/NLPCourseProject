


In this project we use NLP techniques to complete the following task: given a (textual) movie review, determine whether it's positive of negative.
In this project we implemented 5 different neural network models to perform sentiment analysis.

The outcome of this project is a simple web application that allows submitting movie reviews, and then it automatically deducts a rating on a scale of 1 to 10 from that review.

Execution instructions
-

* Use Python 3 to execute the server (Keras and numpy packages are required):
```
> cd server
> python http_server.py
```
* Open index.html in a web browser to use the web application:
Go to the folder "client" and double click on the file "index.html".

* Use the web application to submit IMDb movie reviews and see our NLP engine's analysis results.
The color of the review is ranging from red (bad review), through orange and up to green (good review). You can also place the mouse indicator over the displayed review to see its rating as produced by our NLP engine.

* Look at the outputs of the server Python script to learn about the exact results of each of the models in our combined model.

* The models are ready and serialized in files in server/models.
The code that generates these models can be found in server/models/models_creator.py.
This code was written and executed in Google Colab.