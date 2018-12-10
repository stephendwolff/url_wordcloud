# URL Wordcloud

Generate a wordcloud in a browser from a user supplied URL

## Getting started

```$ docker-compose up```

Open browser [http://localhost:8888/](http://localhost:8888/)

## Prerequisites

Two pieces of software are required to run the project, and an internet connection

1. Docker
2. A web browser, Chrome was used in development

## Running the tests

``` 
$ docker-compose -f docker-compose-test.yml up --build

```

## Overview

The project displays a homepage and admin area using the Tornado framework, and accepts a websocket connection 
for the collection of a valid URL, and to return a word frequency dictionary to the browser asynchronously.

The raw HTMl is processed through BeautifulSoup and some regular expressions before being ordered and placed in a 
python dictionary ready for translating into JSON to be returned to the browser.

The browser displays a word cloud using an edited version of Jason Davies's 'WordCloud' d3 plugin.

The admin area is accessible at [http://localhost:8888/admin/](http://localhost:8888/admin/), and requires only a name
via a login page for viewing a list of words ordered in reverse frequency order.

SQLAlchemy is used for database access, via tornado-alchemy to add asynchronous syntactic sugar.

Encryption is handled by the NaCL library to ensure a high quality of cryptographic practice.

## TODO

* Use SASS pipeline for CSS
* Investigate whether Tornado has named URLs
* Expand admin authentication, beyond simple enter name
* Implement javascript reconnection strategies for websocket handlers
* Split up incoming url word count handling, into reusable functional parts
* Improve punctuation and end-of-line character handling when splitting up words
* Use ntlk for stopwords (including automatic retrieval of data on app start up)
* Add wit.ai sentiment analysis, storage and display
* Improve salted-hashed primary key words, storing random salt with them, instead of hard-coded salt
* Improve SQL insert/update using SQLAlchemy merge
* Split dev requirements into dev and test (including test in dev)
* Get public/private key paths from cmd-line options

## Deployment

The project is not production ready.
 
Currently a public/private key pair is generated on startup if no keys are found in the project root directory.
In order to prepare for a production deployment a key management solution needs to be found, such as a deployment vault, 
with limited access to specific team members, and a process for managing changes of team members.

One possibility would be to have any production secrets (ie secret files, database passwords, SSL certificates) 
encrypted using GPG keys for the team members, and held encrypted in a specific deployment repository. This repository 
would have the necessary scripting (using a deployment tool such as Ansible) to extact the keys on deployment, and to
ensure that deployments are 'idempotent', ie repeatable and consistent.

## Built With

* Tornado
* BeautifulSoup4
* NaCl 
* SQLAlchemy, 
* tornado-sqlalchemy

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/stephendwolff/url_wordcloud/tags). 

## Authors

* **[Stephen Wolff](https://github.com/stephendwolff)**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

Tools used in rendering this package:

* [Cookiecutter](https://github.com/audreyr/cookiecutter)
* [cookiecutter-tornado](https://github.com/hkage/cookiecutter-tornado)
* [Jason Davies](https://jasondavies.com) - D3 wordcloud
