# MessMate Flask project

## Run on Windows / VS Code

1. Install Python if it is not installed.
2. Extract this ZIP and open the `MessMate_Flask` folder in VS Code.
3. Open Terminal in VS Code.
4. Install Flask:

   ```bash
   py -m pip install flask
   ```

5. Start the app:

   ```bash
   py app.py
   ```

6. Open the local address printed in the terminal, usually `http://127.0.0.1:5000`.

## Important notes

- `app.py` contains the Python backend.
- `templates/index.html` contains the website interface.
- This demo stores values in memory, so data resets when the server restarts.
- It is not yet a multi-user real-time system: for that, add a database and a shared deployment/WebSocket or polling setup.
- Tailwind, Google Fonts, and Font Awesome are loaded from online CDNs, so the visual styling requires an internet connection.
