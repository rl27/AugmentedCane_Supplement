`flask_app.py` is a bandaid solution for our need to be able to run CMA-ES personalization experiments using our app without needing to take the phone from the person using it.

A server running `flask_app.py` receives various HTTP requests from the app (which are done automatically) and from another device (which are done manually). In our case, we're running the app on pythonanywhere.

A typical workflow for a heading error experiment looks like this:

1. An experiment is set up. For example, a participant is blindfolded and given a phone to partake in a heading-following experiment. The heading system has 4 parameters that will be tuned/personalized for the participant.
2. The investigator enters `[]/submit?trial=0` in their browser, where `[]` is replaced by the server URL (e.g. `raymondl.pythonanywhere.com`). The server saves this `trial` command, which will start a trial heading experiment.
3. Once every few seconds, the phone app pings `[]/retrieve`. Since there is a saved `trial` command, the server sends back an HTTP response with this command and it is deleted from the server.
4. The phone begins a heading-following trial and the participant completes it. The system automatically calculates an value representing some error metric for that trial. This value is input to the on-device CMA system, which then generates a new set of 4 parameters for the heading system to use in the next trial.
5. The app automatically sends the CMA data from the latest iteration to the server via `[]/append`. This data consists of:
        1. The inputs (system parameters) for the latest iteration
        2. The outputs (recorded times) for the latest iteration
        3. The mean values for each parameter in the CMA system (these change every generation)
        4. The sigma value of the CMA system (this changes every generation)
        5. The seed used for the random number generator in the CMA system.
        6. A file name. This is named after the seed.
6. The server appends this data to a file with the given file name. If the seed is `1504720458`, then the data is appended to `CMA_1504720458.json`. Sending data to `[]/append` and having it saved at each iteration ensures that it's saved in case something goes wrong.
7. For each trial of the heading-following experiment, the app records the user heading and target heading during each frame, then sends that to the server to be saved.
8. Repeat steps 2-7 until you've done the desired number of trials.
9. Take the phone and hit the button on the screen that says "Log". This sends the full set of data to the server. This data is stored in a `.json` file named after the timestamp when the data was received as well as the seed. An example filename is `2024-01-14_17-03-08_1504720458.json`. The name of this file indicates it was created on Jan 14, 2024 at 17:03:08 UTC, with the seed `1504720458`. It should be identical to `1504720458.json`.

Afterwards, if you want to continue optimizing where you left off, the parameters are saved in the phone. You can simply repeat the process above.

---

At some point you may want to do some validation runs to compare the default parameters to the optimized parameters. In order to set the parameters to (for example) `3.5, 2.5, 1.5, 0.5`, do `[]/submit?params=3.5,2.5,1.5,0.5`. This will trigger the same process described above, where the server saves these values in `command.json` and the phone pings the server to retrieve them.

---

Currently there is a button on the app that says "Reset CMA" that will reset the CMA system to its default state. If you ever press this button or otherwise alter the state of the system, use `[]/submit?file=[X]&count=[Y]` to reconstruct a previous state.

Replace `[X]` with the name of a `.json` file containing CMA data. This could be `1504720458` for `1504720458.json` or `2024-01-14_17-03-08_1504720458` for `2024-01-14_17-03-08_1504720458.json`. Replace `[Y]` with an integer representing the number of CMA iterations.
* For example, if you previously did 64 runs/iterations and wish to set the system to its state after the 32nd iteration, enter `[]/submit?file=2024-01-14_17-03-08_1504720458&count=32`.
* If you want to get it to its state at the latest iteration, do `[]/submit?file=2024-01-14_17-03-08_1504720458&count=64`.