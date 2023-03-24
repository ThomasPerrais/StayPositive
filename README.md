
# StayPositive 🤗

## Introducing StayPositive

This simple app is intended to help people focus on the good things that happen in the everyday life, no matter the rest.

## Running StayPositive

The cleanest way to run the app is using docker-compose.

The app uses Elasticsearch to store the moments which should be deployed in a separate container.

Use the docker-compose.yml file by running
```
docker-compose up -d
```

When first using the app you should create a 'moments' index in Elasticsearch by running the following in a command prompt
```
curl -X PUT "localhost:9200/moments?pretty" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 1
  },
  "mappings": {
    "properties": {
      "text": { "type": "text" },
      "date": { "type": "date" }
    }
  }
}
```

You're all set!

*Note*: in a futur release we will add a 'User' page to the app to login and this will handle the index creation.