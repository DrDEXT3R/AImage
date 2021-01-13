[![Contributors][contributors-shield]][contributors-url]
[![AGPL License][license-shield]][license-url]
[![Release][release-shield]][release-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a>
    <img src="doc/logo.png" alt="Logo" width="50" height="50">
  </a>
  <h1 align="center">AImage</h1>
  <p align="center">
    <a href="https://github.com/DrDEXT3R/AImage/"><strong>Project Link »</strong></a>
  </p>
</p>


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#demo">Demo</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#features">Features</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#workflow">Workflow</a></li>
    <li>
      <a href="#implementation-description">Implementation Description</a>
      <ul>
        <li><a href="#google-drive">Google Drive</a></li>
        <li><a href="#docker">Docker</a></li>
      </ul>
    </li>
    <li><a href="#authors">Authors</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project
Web application that allows User to improve the quality of low-resolution images using the deep learning model. 
The logged in User can also store images before and after improving on the server.

### Demo
#### Desktop Version
![Computer](doc/desktop.gif) 
#### Mobile Version
![Mobile](doc/mobile1.png)
![Mobile](doc/mobile2.png)
#### Result
TODO  
![Result](doc/logo.png)

### Built With
* [Python 3](https://docs.python.org/3/) - a programming language
* [HTML](https://html.spec.whatwg.org/multipage/) - a language for describing the structure of websites
* [Sass](https://sass-lang.com/documentation) - a stylesheet language that is compiled to CSS
* [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) - a programming language that allows you to implement complex features on web pages
* [Django](https://docs.djangoproject.com/en/3.1/) - a high-level Python Web framework
* [Docker](https://docs.docker.com/) - a containerization technology
* [Bootstrap](https://getbootstrap.com/docs/4.5/getting-started/introduction/) - a framework for developing responsive and mobile-first websites
* [Neural Enhance](https://github.com/alexjc/neural-enhance) - a deep learning model


<!-- FEATURES -->
## Features

- **User registration and login**
- **Logged in User feauters**:
  - Storing images on the server
  - Loading images from disk, by entering a URL or from Google Drive
  - Improving images stored on the server using the neural network
  - Improving images without saving them to the server using the neural network
  - Adding feedback on image processing results
- **Not logged in User feauters**:
  - Improving images (with a size limit) using the neural network without being able to save images to the server 
- **"Contact" tab with the access map**

<!-- GETTING STARTED -->
## Getting Started

These instructions allow you to run a copy of the project on your local computer for programming and testing purposes.

### Prerequisites
1. Python 3
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3.8
sudo apt-get install python3-pip
```
2. Docker  
TODO
3. etc  
TODO

### Installation
1. Clone the repo
```sh
git clone https://github.com/DrDEXT3R/AImage.git
```
2. Install the necessary dependencies
```sh
pip install -r requirements.txt
```
3. Create database
```sh
cd aimagesite
python manage.py makemigrations
python manage.py migrate
```
In our project we use sqlite3 database. If you want to use different kind of database it's no problem, because Django uses ORM. 
All you have to do is change the database settings in the aimagesite/aimagesite/settings.py file:   
![Database settings](doc/db_settings.png)

4. Run local server
```sh
python manage.py runserver
```
5. Open local server  
http://127.0.0.1:8000/

TODO docker

<!-- WORKFLOW -->
## Workflow
1. See the [Issues](https://github.com/DrDEXT3R/AImage/issues) and the [Projects](https://github.com/DrDEXT3R/AImage/projects) sections.
2. Make changes
3. Open a Pull Request

### Branches
Code Flow Branches:
- Master - ```master```  
The branch with the last working version of the project. 
- Development - ```develop```  
The main branch on which users' work is assembled.

Temporary Branches:
- Feature - ```feature/branch-name```  
A branch on which all work related to software implementation is performed.
- Release - ```release/branch-name```  
A preparatory branch for the release of the project version.
- Bug Fix - ```bugfix/branch-name```  
This is a fix that needs to be implemented.
- Hot Fix - ```hotfix/branch-name```  
This is a fix that must be included in the project version as soon as possible.


<!-- IMPLEMENTATION DESCRIPTION -->
## Implementation Description

TODO
### Google Drive
Description / steps / code

### Docker
Description / steps / code

### etc


<!-- AUTHORS -->
## Authors

* **Tomasz Strzoda** - [DrDEXT3R](https://github.com/DrDEXT3R)
* **Dawid Macha** - [diejdablju](https://github.com/diejdablju)
* **Marek Hermansa** - [marekhermansa](https://github.com/marekhermansa)


<!-- LICENSE -->
## License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [alexjc](https://github.com/alexjc)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/DrDEXT3R/AImage?color=blue&style=for-the-badge
[contributors-url]: https://github.com/DrDEXT3R/AImage/graphs/contributors
[license-shield]: https://img.shields.io/github/license/DrDEXT3R/AImage?style=for-the-badge
[license-url]: https://github.com/DrDEXT3R/AImage/blob/master/LICENSE
[release-shield]: https://img.shields.io/github/v/release/DrDEXT3R/AImage?style=for-the-badge
[release-url]: https://github.com/DrDEXT3R/AImage/releases