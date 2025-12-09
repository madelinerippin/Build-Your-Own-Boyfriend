# Partner Builder

## What Our System Is:
We created a story generation application based off the Plan-and-Write approach; however instead of using keywords to generate a story we are using different romance tropes (2-4) to create a story. Our system collects user input of their name/gender, love interest’s name/gender, love interest details, what tones they want to see within the story, and the story tropes. Upon clicking the story trope, users will have the ability to modify pre-determined beats for each trope (add, remove, move). Our goal for this project was to make a fun and creative experience catered to the user. Enjoy!

## What It's Supposed To Do
The ultimate goal of our system is to create a story based on user-selected romance tropes and preferences. After collecting all the user input from the frontend, we send it to the backend to assess trope compatibility (if the user tries to do Friends to Lovers and Enemies to Lovers in the same story, they are reprompted to select again). If that's successful, then we prompt chatgpt-4.1-nano to create a section of the story for each trope selected. We make a final call to the model to ensure the story is coherent, display it for the user, and save it as one of their generated stories to view at their leisure. 

## How to Setup and Run Demo:
Step 1: Clone the repository ```github clone https://github.com/madelinerippin/Build-Your-Own-Boyfriend.git```

Step 2: Create a `.env` file with a var called OPENAI_API_KEY set to your OpenAI API key

Step 3: Install dependencies ```pip install -r requirements.txt```

Step 4: Run the file ```python -m uvicorn new_partner_builder:app --reload``` (make sure you are in the Backend directory)

Step 5: Make a new terminal and run ```open "[file-path]/index.html"``` for Mac/Linux and ```start "[file-path]/index.html"```

Step 6: Insert all user input and then click the "Generate" button to see your created story!
