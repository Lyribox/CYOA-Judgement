The CYOA_Judgement game was built using Flask, Python, Javascript, and jQuery on VS Codespaces. The game was built on 7 html pages. 4 of which are related to the story. Due to the dynamic and short nature of the storyline, I found it better to restrict players from continuing from any point. The only way to play is to make a new registry every time. This way, one can see how many attempts there have been.

There are 3 main html pages containing a lot of the story. The story was split into several parts and embedded into divs. Each div was connected to and influenced the next one, this mode of connecting the narrative was inspired by linked lists. There was the option to split every variation of the story into separate html pages. While easier to build, this would have been very chaotic and messy. It would also inconvenience the player to wait for loading each and every time they made a decision.

Following that, I set the default attribute of the divs to be hidden. And then attached a function to each link at the end of its div which would unveil the next one. The 'continue' links only unhid the following div. However, the multiple choice divs had specific divs which they influeced. Once a player picked an option, the corresponding div would be unveiled (some had more conditions to be met to reveal).

Majority of the functions affecting the variables are coded to only trigger once. This is to minimize 'creativity' among the players.

In order to manage the impact of the choices made in a single playthrough, I created a table in the database that would attach itself to the session and keep track of the variables between the pages. Managing the variables across various routes was truly a test of dictionary management and JSON. Facilitating communication between the Flask server and the Javascript was incredibly difficult.

Initially, I had designed each page with various backgrounds. However, I found it distracting from the story and slightly offputting. To maintain the eerie feeling developed throughout the story, I kept the backgrounds blank and desolate.