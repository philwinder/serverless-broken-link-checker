# serverless-broken-link-checker

A severless (AWS Lambda) broken link checker for checking 403/404/500s
on websites.

This is a Python serverless-based project to create a lambda on AWS
running as a daily cron job. The goal is to scrape a website and check
that all links are valid (i.e. no 403s, 404s, 500s and 501s).

It scrapes your website using the `scrapy` Python library. The crawler
will follow all internal links on your website. All external URLs are
checked, but are not followed. After the crawler has finished it will
send an email using `mailgun`s REST API.

It shouldn't be too hard to convert this to use another cloud provider.

## Requirements

- AWS account (see [serverless quick start](https://serverless.com/framework/docs/getting-started/))
- Mailgun account

## Prerequisites

1. Node.js (tested with v6.11.4)
2. [Serverless](https://serverless.com) (tested with 1.24.1)
3. Python3 (tested with 3.6.2)

## Installation

```bash
npm install
serverless plugin install -n serverless-python-requirements
```

## Build

You will need to export the required settings and secrets.

```bash
export MAILGUN_API_KEY=key-xxxx MAILGUN_DOMAIN_NAME=example.com EMAIL=test@example.com URL=https://example.com  
serverless deploy
```

## Usage

The code is set to run every 24 hours. But you can run it manually with:

```bash
serverless invoke -f cron
```

## Configuration

The following environmental variables are exposed. You must set these
before you run `serverless deploy`.

- **MAILGUN_API_KEY**: Your mailgun API key
- **MAILGUN_DOMAIN_NAME**: Your mailgun domain name
- **EMAIL**: The email address you want to send the report to
- **URL**: The URL you want to check (in the format: `https://example.com/`)
