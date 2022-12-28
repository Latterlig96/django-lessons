[![lint](https://github.com/Latterlig96/django-lessons/actions/workflows/lint.yml/badge.svg)](https://github.com/Latterlig96/django-lessons/actions/workflows/lint.yml)
[![test](https://github.com/Latterlig96/django-lessons/actions/workflows/test.yml/badge.svg)](https://github.com/Latterlig96/django-lessons/actions/workflows/test.yml)

## **Django Lessons**

This project aims to create a learning platform for both student and tutors to communicate with each other, share exercises and constantly improving their skills regarding given domain of interest.

## Prerequisites
* Installed docker with version 20.10.12
* Installed docker compose with version v2.2.3
* Python version >= 3.9
* Pipenv installed to manage dependencies

## How to run
* Adjust `.env` file with appropriate values (project has some integrations with third-party platform to increase fuctionality such as `stripe` or `daphne` so this tweaking is needed)
* Run production environment using docker with command `docker-compose up --build`
* After creation of this environment you can adjust some models with data of your choice and test it by yourself ! :)

## Dev server
* To run development server (with limited functionality) just deploy it with docker using command `docker build --tag django-lessons:latest --network host -f docker/Dockerfile.dev .` and then `docker run -p 8000:8000 django-lessons:latest`. (Please note that appropariate port should be open when binding to port in container so appropriate tweak of port might be needed when deploying dev server).
* After creation of dev user default superuser will be created (refer to [docker-django-entrypoint-dev.sh](/scripts/docker-django-entrypoint-dev.sh)) that can be used to propagate website with simple data to test functionality.

## Functionality
* **Admin page**
* **Being able to authenticate both as a student and as a tutor**
* **Password reset**
* **Account settings reset** 
* **Different functionality based on your role (as a tutor you have possibility to create messages for students and also simple live chat rooms to chat with students on demand)**
* **Activitiy monitor**
* **Ability to create premium exercises that will be targeted only for premium student users**
* **Integration with payment gateway ([stripe](https://stripe.com/en-pl)) to buy subscription to become premium student.**
* **Integration with websocket gateway ([channels](https://channels.readthedocs.io/en/stable/)) to create live chat rooms for students and tutors**
* **Redis as a backend for websocket gateway**
* **Nginx deployment on production build**
* **Postgresql as a backend on production build**
* **S3 integration with the use of open source solution ([minio](https://min.io/hybrid-cloud-storage?utm_term=&utm_campaign=Multi+Cloud+1.0&utm_source=adwords&utm_medium=ppc&hsa_acc=8976569894&hsa_cam=13555764414&hsa_grp=124202627221&hsa_ad=546403830688&hsa_src=g&hsa_tgt=dsa-1426483338857&hsa_kw=&hsa_mt=&hsa_net=adwords&hsa_ver=3)) that can be easily changed to work with other cloud provisioners**
* **CI pipeline for both linting and testing**

## Tech stack
* **Django** <img src=".github/.idea/django.svg.png" width=150></img>
* **Django channels** <img src=".github/.idea/django_channels.webp" width=150>
* **Stripe** <img src=".github/.idea/stripe.svg" width=150>
* **Docker** <img src=".github/.idea/docker.svg.png" width=150>
* **S3** <img src=".github/.idea/s3.svg" width=60> 
* **Postgresql** <img src=".github/.idea/postgresql.svg.png" width=60>
* **Redis** <img src=".github/.idea/redis.svg.png" width=150>
* **Nginx** <img src=".github/.idea/nginx.svg.png" width=150>

## Further improvmenets

* Improve frontend design. If some frontend developers read this repository I'm open for a collaboration cause given the fact that this repository was created mostly for a backend development I don't focus much on front design so it might need some further adjustments.
* Heroku deployment. With the given docker deployment it might be easy to improve it as a live application but regarding first point I do not plan to make it since I don't feel the application looks good on front.