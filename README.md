# UIUC Kappa Theta Tau &middot; [![Netlify Status](https://api.netlify.com/api/v1/badges/665a9b40-0c4f-4dc7-88a5-f995f164db6e/deploy-status)](https://app.netlify.com/sites/kappathetatau/deploys)

This is the documentation for Kappa Theta Tau's main website.

# Table of contents

- [Cloning](#cloning)
- [Pushing Changes](#pushing-changes)
- [Updating Contacts](#updating-contacts)
- [Updating Brothers](#updating-brothers)
- [Development](#development)
  _ [System Preparation](#system-preparation)
  _ [Local Installation](#local-installation)
  _ [Usage](#usage)
  _ [Deploy](#deploy-with-gulp)

## Cloning

To clone this repo, simply git clone and cd into it.

```shell
$ git clone https://github.com/KappaThetaTau/kappathetatau.github.io.git & cd kappathetatau.github.io
```

## Pushing Changes

We are using github-pages to automatically compile and host our website. This means that to update the website, you simply need to push changes to your own branch and make a pull request on Github.

```shell
$ git checkout -b <new branch name>
...
<work on the website>
...
$ git add <whatever changes you made>
$ git commit -m "<meaningful commit message"
$ git push origin <new branch name>
<go make your pull request!>
```

## Updating Contacts

Contacts are managed by a CSV file located [here](_data/contacts.csv). To edit the contacts, simply edit this file

```shell
$ open _data/contacts.csv
```

## Updating Brothers

To update the [brothers](brothers.html) page we use a python [script](scripts/update_data.py) to pull the brother information and images from a google form CSV (https://forms.gle/PsYvMq74Y2J73mUo6).

```shell
$ python scripts/update_data.py
```

## Development

### System Preparation

1. [Ruby 2.3.6](https://rvm.io/)
2. [NodeJS 6.17.1](https://github.com/nvm-sh/nvm)
3. [GulpJS](https://github.com/gulpjs/gulp) - `$ npm install -g gulp` (mac users may need sudo)

### Local Installation

1. Clone this repo, or download it into a directory of your choice.
2. Inside the directory, run `nvm use`.
3. Inside the directory, run `npm install`.
4. Inside the directory, run `bundle install`.

### Usage

**development mode**

This will give you file watching, browser synchronisation, auto-rebuild, CSS injecting etc etc.

```shell
$ gulp
```

**jekyll**

As this is just a Jekyll project, you can use any of the commands listed in their [docs](http://jekyllrb.com/docs/usage/)

## Contact

- Current Web Chair: Jeff Taylor-Chang &middot; thetatauwebchair@gmail.com
- Previous Web Chair: Dylan Huang &middot; dylan.p.huang@gmail.com
