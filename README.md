# PARKEE_TechnicalTest_Kyosena

To start the app, the system must have a docker engine installed and running, with docker-compose support. With the prerequisites installed, run the following command:
### `docker-compose up -d --build`
The following command will build 3 images and run 3 containers from those images. Should you wish to look at the logs while it is running, remove the '-d' flag and run
### `docker-compose up --build`
Note that in this case, the application will quit when you exit the terminal.
## Migrating database

Should the database migrate script not run properly (indicated by database errors while interacting with the API), then migrating the database is necessary.
Firstly, find the container_ID of the django app. Do so by running the following command:
### `docker container ls | grep parkee`
3 containers should be listed. Copy the container_id of *parkee_web* (the container_id is the colomn on the left), and run:
### `docker container exec -it <container_id> bash`
Once inside the container, run the command:
### `python3 manage.py migrate`
The app should now run properly.
