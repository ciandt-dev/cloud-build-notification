# HOW TO USE THIS CLOUD FUNCTION

## Create a .env.yaml file containing the Slack token and channel

```
SLACK_TOKEN: my-slack-token
SLACK_CHANNEL: my-slack-channel
```

## Deploy the function

```
gcloud functions deploy cloud_build_notification --runtime python37 --trigger-topic cloud-builds --project <my-project> --env-vars-file .env.yaml
```
