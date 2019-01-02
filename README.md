## Just Blog - Fullstack Blog Project
---
### Installation and Setup
Install [Python 2.7](https://www.python.org/download/releases/2.7/) and [pip](https://pypi.python.org/pypi/pip) and clone this project:

    $ mkdir ~/just-blog
    $ cd ~/just-blog
    $ git clone https://github.com/namdaoduy/blog-backend.git blog-backend

Set up [Virtualenv](https://virtualenv.pypa.io/en/stable/):

    $ pip install virtualenv
    $ cd ~/
    $ virtualenv env
    $ source ~/env/bin/activate

Install project dependencies:

    $ cd ~/just-blog/blog-backend
    $ pip install -r requirements.txt
    
### Database Setup and Configuration

Install [mysql 5.7](https://dev.mysql.com/downloads/mysql/5.7.html) and run the server:

    $ mysql.server start

Create a local development database:

    $ mysql -u root
    mysql> create database just-blog

Run database migrations:

    $ python database_setup.py
    
### Local Development

To start an instance of the server running on your local machine:

    $ python run.py
