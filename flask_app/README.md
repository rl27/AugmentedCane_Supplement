`flask_app.py` is a bandaid solution for our need to be able to run CMA-ES personalization experiments using our app without needing to take the phone from the person using it.

A server running `flask_app.py` receives various HTTP requests from the app (which are done automatically) and from another device (which are done manually.) In our case, we're running the app on pythonanywhere.

A typical workflow looks like this:

1. An experiment is set up. For example, a large cardboard hallway is set up and a participant must navigate the hallway with the obstacle avoidance system active. The obstacle avoidance system has 4 parameters that will be tuned/personalized for the participant.
2. The participant navigates the hallway once; the investigator records the time they take. Let's say it took 11.57 seconds. We need the phone to receive this value. This is where our bandaid `flask_app` comes into play.
    1. The investigator enters `[]/submit?sample=11.57` in their browser, where `[]` is replaced by the server URL. In our case, `[]` would be replaced by `raymondl.pythonanywhere.com`. The server creates a file named `command.json` and saves the value there.
    2. Once every few seconds, the phone app pings `[]/retrieve`. If there is a value in `command.json` (e.g. 11.57), the server sends back an HTTP response that value and empties `command.json`.
    3. The phone app receives 11.57 and enters that into the on-app system for running CMA. The CMA system generates a new set of 4 parameters for the obstacle avoidance system to use in the next run through the hallway.
    4. The app automatically sends the latest CMA data to the server via `[]/append`. This data consists of:
        1. The inputs (system parameters) for the latest iteration
        2. The outputs (recorded times) for the latest iteration
        3. The mean values for each parameter in the CMA system (these change every generation)
        4. The sigma value of the CMA system (this changes every generation)
        5. The seed used for the random number generator in the CMA system.
    10. The server appends this data to a file named after the seed. If the seed is `1504720458`, then the data is appended to `1504720458.json`. Sending data to `[]/append` and having it saved at each iteration ensures that it's saved in case something goes wrong.
4. Repeat step 2 until you've done the desired number of trials.
5. Take the phone and hit the button on the screen that says "Log". This sends the full set of data to the server. This data is stored in a `.json` file named after the timestamp when the data was received as well as the seed. An example filename is `2024-01-14_17-03-08_1504720458.json`. The name of this file indicates it was created on Jan 14, 2024 at 17:03:08 UTC, with the seed `1504720458`. It should be identical to `1504720458.json`.

Afterwards, if you want to continue optimizing where you left off, the parameters are saved in the phone. You can simply repeat the process above.

---

At some point you may want to do some validation runs to compare the default parameters to the optimized parameters. In order to set the parameters to (for example) `3.5, 2.5, 1.5, 0.5`, do `[]/submit?params=3.5,2.5,1.5,0.5`. This will trigger the same process described above, where the server saves these values in `command.json` and the phone pings the server to retrieve them.

---

Currently there is a button on the app that says "Reset CMA" that will reset the CMA system to its default state. If you ever press this button or otherwise alter the state of the system, use `[]/submit?file=[X]&count=[Y]` to reconstruct a previous state.

Replace `[X]` with the name of a `.json` file containing CMA data. This could be `1504720458` for `1504720458.json` or `2024-01-14_17-03-08_1504720458` for `2024-01-14_17-03-08_1504720458.json`. Replace `[Y]` with an integer representing the number of CMA iterations.
* For example, if you previously did 64 runs/iterations and wish to set the system to its state after the 32nd iteration, enter `[]/submit?file=2024-01-14_17-03-08_1504720458&count=32`.
* If you want to get it to its state at the latest iteration, do `[]/submit?file=2024-01-14_17-03-08_1504720458&count=64`.

---

To run a trial for the heading error experiment, do `[]/submit?trial=0`. The value of the number doesn't matter.