# Frisbee Focus

I hope you like our app. This project was for an internship Dharunraj Nagarajan has, and Wissam is "teamed" to make sure all the files are saved, optomized, and no hiccups happen.


##  Quick Links

> - [ Overview](#overview)
> - [ Features](#features)
> - [ Repository Structure](#repository-structure)
> - [ Modules](#modules)
> - [ Getting Started](#getting-started)
>   - [ Installation](#installation)
>   - [ Running ](#running)
> - [ Contributing](#contributing)
> - [ Acknowledgments](#acknowledgments)

---

##  Overview

FrisbeeFocus is a web application that enables users to submit frisbee throw videos, which it analyzes and provides nuanced AI-generated feedback. Leveraging OpenAI's GPT-4 model, the application offers actionable, personalized advice, integrating varied context like throw type and weather conditions. The app ensures environment and build consistency, integrates robust logging features, and maintains user-friendly, aesthetically pleasing UI.

---

##  Features

|    |   Feature         | Description |
|----|-------------------|---------------------------------------------------------------|
| ⚙️  | **Architecture**  | The project revolves around a Flask web application that uses SSH for server communication and OpenAI for AI functionalities to analyze frisbee throws |
| 🔩 | **Code Quality**  | Code is concise and well-structured, following best practices for Python development and ensuring readability and maintainability |
| 📄 | **Documentation** | The project lacks comprehensive documentation but each key file contains clear and descriptive comments. This README file should make up for it as well lol. |
| 🔌 | **Integrations**  | Integrated with Paramiko for SSH communication, Flask for webserver capabilities and OpenAI's GPT-4 model for AI functionalities. |
| 🧩 | **Modularity**    | Modularity is achieved via the segregation of responsibilities in different directories and files. |
| ⚡️  | **Performance**   | Efficient usage of server resources. The Flask app should be relatively fast and light on resource usage. |
| 🛡️ | **Security**      | OpenAI API credentials are being managed and secured, although no explicit security measures are mentioned. |
| 📦 | **Dependencies**  | Major dependencies include Flask, Paramiko, OpenAI, Jinja2 and requests among others. Managed using `poetry.lock` and `requirements.txt`. |


---

##  Repository Structure

```sh
└── /
    ├── main (copy).py
    ├── main.py
    ├── poetry.lock
    ├── pyproject.toml
    ├── replit.nix
    ├── requirements.txt
    └── templates
        └── index.html
```

---

##  Modules

<details closed><summary>File Summaries</summary>

| File                                                                                       | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ---                                                                                        | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| [main.py](https://github.com/MayFly404/FrisbeeFocus/blob/master/main.py)                   | This script controls a web application that communicates with a remote server via SSH. It utilizes Flask for the web aspect, Paramiko for SSH communication, and openai for AI-related functionalities. The app can send commands to the remote server and includes robust logging features. It also manages an uploads directory and secures OpenAI API credentials.                                                                                                                                                                                                |
| [replit.nix](https://github.com/MayFly404/FrisbeeFocus/blob/master/replit.nix)             | The replit.nix file in the repository is responsible for managing system-level dependencies. It helps ensure that necessary libraries (libGLU, libGL, openssh) are pre-installed on the server, thus providing environment consistency across different deployment stages.                                                                                                                                                                                                                                                                                           |
| [poetry.lock](https://github.com/MayFly404/FrisbeeFocus/blob/master/poetry.lock)           | The poetry.lock file in this repository is critical for dependency management. It freezes the project's Python dependencies, ensuring consistent and predictable builds by locking each package to a specific version.                                                                                                                                                                                                                                                                                                                                               |
| [main (copy).py](https://github.com/MayFly404/FrisbeeFocus/blob/master/main (copy).py)     | This code forms the core of a Flask application that receives a video of a frisbee throw via an API endpoint, extracts frames from the video, and analyzes them. After the frame analysis, the system utilizes the OpenAI GPT-4 model to generate a natural language feedback based on frame summaries and additional context like weather and throw type. This feedback then gets sent back to the client as a response. The critical feature accomplished here is leveraging an AI model to provide actionable, user-friendly feedback about user-uploaded videos. |
| [pyproject.toml](https://github.com/MayFly404/FrisbeeFocus/blob/master/pyproject.toml)     | This `pyproject.toml` file serves as a configuration file for the python project. It outlines key metadata about the project such as its name, version, and author. More notably, it specifies the project dependencies and associated versions, like Flask and OpenAI. Additionally, it configures the build system and Python linting preferences.                                                                                                                                                                                                                 |
| [requirements.txt](https://github.com/MayFly404/FrisbeeFocus/blob/master/requirements.txt) | The requirements.txt file lists the Python dependencies required by the project. It specifies packages like Flask for web server capabilities, Jinja2 for HTML templating, and requests for HTTP requests management, crucial for the application's functionality following the repository's architecture.                                                                                                                                                                                                                                                           |

</details>

<details closed><summary>templates</summary>

| File                                                                                     | Summary                                                                                                                                                                                                                  |
| ---                                                                                      | ---                                                                                                                                                                                                                      |
| [index.html](https://github.com/MayFly404/FrisbeeFocus/blob/master/templates/index.html) | The code in templates/index.html constructs the user interface for the FrisbeeFocus GPT application. It styles and structures the primary webpage, creating a responsive, centered container in a dark-themed aesthetic. |

</details>

---

##  Getting Started

***Requirements***

Ensure you have the following dependencies installed on your system:

* **Python** >=`version 3.8.x`

###  Installation

1. Clone the  repository:

```sh
git clone https://github.com/MayFly404/FrisbeeFocus/
```

2. Change to the project directory:

```sh
cd 
```

3. Install the dependencies:

```sh
pip install -r requirements.txt
```

###  Running 

Use the following command to run :

```sh
python main.py
```


##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/MayFly404/FrisbeeFocus/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/MayFly404/FrisbeeFocus/discussions)**: Share your insights, provide feedback, or ask questions.
- **[Report Issues](https://github.com/MayFly404/FrisbeeFocus/issues)**: Submit bugs found or log feature requests for .

<details closed>
    <summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.
   ```sh
   git clone https://github.com/MayFly404/FrisbeeFocus/
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

---

##  Acknowledgments

Dharunraj Nagarajan was responsible for the AI implementation, Wissam Nusair was responsible for attatching the remote server, file optimization, and storage optimization.

[**Return**](#-quick-links)
