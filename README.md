# PLUTO
Pluto is a subscription manager webapp.

## Installation

```bash
pip install PlutoManager
```

## Project structure

- flakProject
    - instance
      - mindenszipiszuper.db
    - static
        - css
        - Photos
    - templates
        - base.html
        - index.html
        - input.html
        - main.html
        - profile.html
        - registration_completed.html
        - registration_page.html
        - statistics.html
  - testing
  - venv
- app.py
- models.py
- requirements.txt

## How to use

### Launching and opening webpage

To launch the web application run the app.py file in your IDE of choice or run the following command in a terminal:

```bash
RouteToTheProject\flaskProject\venv\Scripts\python.exe -m flask run
```

To access the webpage click the following URL displayed in the terminal after launching the application:

```bash
http://127.0.0.1:5000
```

Or copy and paste this URL in the browser of choice.

### Usage guide

After opening the project in a browser, the first page the user sees is the index.html page. On this page the user has two options: logging in and registration. 

Clicking on the registration button the user will be taken to registration_page.html where they have to fill out their username and password. Duplicate and short usernames are not allowed. If registration is successful the user will be redirected to another page, from which they can get back to the index page.

After logging in the user will be redirected to the main page. On the main page the user can choose from 4 different actions: inputing their subscriptions, viewing their statistics, viewing their profile and logging out. 

The input page has a form to fill out with the user's subscription information such as: name, price, category, payment type, start date of the subscription. On the right the user can scroll through their already existing subscriptions.

The statistics page displays the user's subscriptions on the right. On the left the user can select filters. The statistics page display a heatmap and different charts.

The profile page displays additional information and statistics about the user's subscriptions. The user can also delete their subscriptions here, one or more at the time. 





