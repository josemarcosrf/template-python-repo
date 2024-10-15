# Template Python Repo

This is a dummy readme for the python repo template.


## How To

To create a new repository using this one as a template, in github
find and click on the `Use this template` green button on the top right corner.

Fill up the details and then clone it locally.

> **note**: Once cloned you'll need to **Rename your package**: Rename the `src/template_python_repo` python module directory and all reference to it


## Local Environment

### Environment variables

> Check [.env.example](.env.example) and update as required.

### Dependencies and Installation

We use [pdm](https://pdm-project.org/latest/#installation) to manage as the python package manager.

The dependencies are organised in groups based on the requirements of each flow separately,
plus the common dependencies that apply to more than one flows.

Because of that, to install all the dependencies use the following command:

```shell
pdm install -G :all
```
