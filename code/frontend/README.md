# Front end

## Run and Test
To open the web app, run the following in your terminal:
```
    cd code/frontend/web-app
    npm run dev
```

## Structure

- This section of the project contains two main directories:
  - Web-app: the actual web app, holding pages and all information that may be displayed to users
    - hosted by web server

## Web App
- Login page: Has elements for registering and logging in (login for generic user and admin)
  - Contains scripts to handle the logging in and verification wrt communication with the server
    - Server handles actual request with database
  - Uses regex to ensure passwords and emails match the correct patterns
  - Does not handle async encryption for passwords
