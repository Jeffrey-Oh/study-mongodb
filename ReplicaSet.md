해당 예제는 `localhost` 에 직접 구성하는 방식으로 진행된다.

`Replica Set` - HA (고가용성), 조회가 빠름 (Read 에 적합)  
`Sharded Cluster` - HA, 쓰기가 많이 발생하는 경우에 적합

두개가 서로의 장단점이 됨

그래서 어플리케이션을 구축할 때 프로젝트의 성격에 맞게 세팅을 정해야하지만 `초기에는 대부분 Replica Set 으로 시작`하여 필요 시 Sharded Cluster 로 수정하는 것을 추천

---

직접 구축할 때는 다음과 같은 폴더가 필요하다 (폴더명은 임의 지정)

-   config : config 설정이 들어있는 각 db 서버 yaml 파일들
-   logs : log 를 남기기 위한 폴더
-   data : data 저장을 위한 폴더

---

### Replica Set

```
./mongod --replSet rs1 --port 27017 --bind_ip "0.0.0.0" --dbpath /Users/user/mongodb/data1 --oplogSize 128
./mongod --replSet rs1 --port 27018 --bind_ip "0.0.0.0" --dbpath /Users/user/mongodb/data2 --oplogSize 128
./mongod --replSet rs1 --port 27019 --bind_ip "0.0.0.0" --dbpath /Users/user/mongodb/data3 --oplogSize 128
```

-   replSet : 레플리카 설정는 옵션이며 그 뒤에는 레플리카 이름
-   port : 할당 포트
-   bind_ip : 접속가능한 ip를 바인딩하는 옵션으로 필수 값 (예제는 0.0.0.0 으로 전체로 지정)
-   dbpath : data 가 저장될 경로를 지정해줌
-   oplogSize : oplog 가 사용할 용량지정

db 서버를 모두 띄웠다면

`Shell Tool` 을 이용하여 접속

```
./mongosh "mongodb://localhost:27017"
```

```
rs.status()
```

위 명령어를 실행해보면 처음에 Replica Set 이 안되어 있어서 아래 에러를 볼 수 있다

```
MongoServerError: no replset config has been received
```

아래의 명령어를 통해 레플리카를 지정한다

```
rs.initiate({
    _id: "rs1",
    members: [
        { _id: 0, host: "localhost:27017" },
        { _id: 1, host: "localhost:27018" },
        { _id: 2, host: "localhost:27019" },
    ],
});
```

그리고 다시 `rs.status()` 명령어를 통해서 확안해보면 primary 1개, secondary 2개가 잡히는 것을 확인할 수 있다

---

명령어를 통한 서버를 실행시킬 때마다 옵션이 다양하기 때문에 이를 yaml 파일로 설정하여 file 단위로 실행할 수 있다

```
net:
    port: 27017
    bindIp: 0.0.0.0

storage:
    dbPath: "/Users/user/mongodb/data1"
    directoryPerDB: true

replication:
    oplogSizeMB: 128
    replSetName: "rs1"

systemLog:
    path: "/Users/user/mongodb/logs/mongod1.log"
    destination: "file"
```

그런 다음 아래 명령어로 서버 개수 만큼 서로 다른 터미널에서 실행 후 레플리카 설정을 하면 끝

```
./mongod -f /Users/user/mongodb/config/mongod1.conf
./mongod -f /Users/user/mongodb/config/mongod2.conf
./mongod -f /Users/user/mongodb/config/mongod3.conf
```

백그라운드에서 실행 되기 때문에 `logs` 쪽에서 `tail -f` 명령어로 실시간 확인이 가능하며

db 서버에 접속하여 아래를 실행하여 마무리

```
rs.initiate({
    _id: "rs1",
    members: [
        { _id: 0, host: "localhost:27017" },
        { _id: 1, host: "localhost:27018" },
        { _id: 2, host: "localhost:27019" },
    ],
});
```