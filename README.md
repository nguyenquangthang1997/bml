Run BML

You must run on three tab separately.

1. Start Sawtooth network:
```shell script
cd bml_sawtooth 
docker-compose up
```
 

2. Start Elasticsearch an IPFS:
```shell script
cd  bml_ipfs
docker-compose up
```

3. Start BML:
```shell script
make
```

