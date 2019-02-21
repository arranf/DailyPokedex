# Daily Pokedex Entry

This is the code for a basic AWS Lambda function written in Python (3.7) which sends a Pokedex entry via SMS and email every day.

## Setup

1. Create a virtual environment to store your Python packages.

```bash
python3 -m v-env
source v-env/bin/activate
pip install
```

2. Create a `.env` file to store your configuration. `cp .env.example .env`
3. Edit the contents of `.env` to include your [Twilio](https://twilio.com) SID, auth token, and from number. Also include your SendGrid API key and the email address and phone number that the Pokedex entry should be sent to.


## Deployment Details

The script must be deployed as a [Python deployment package](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html#python-package-dependencies). To do so, whilst in the virtual environment run `package.sh`.