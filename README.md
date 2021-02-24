# WebPlayer

Build docker container:

```shell
docker build . -t web_player
```

Run docker container from source code directory:

```shell
docker container run -d -v ${PWD}:/WebPlayer -w /WebPlayer -p 8080:8080 --device /dev/snd web_player
```
