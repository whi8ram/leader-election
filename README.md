# leader-election
zookeeper를 활용한 리더 선출 프로그램

## Basic usage

먼저, zookerper 서버를 실행합니다.

```
$ docker-compose -f docker-compose.yml up
```

프로젝트에 필요한 의존성을 설치합니다.

```
$ poetry shell
$ poetry install
```


쉘에 여러개 연결하여 각각 리더 선출 프로그램을 실행시킵니다.

```
$ python src/main.py
```

일부 리더 선출 프로세스를 kill하면서 다른 프로세스의 로그를 확인합니다.

로그 예시:
```
2023-11-02 02:05:41,047 [INFO]: I am not the leader.
2023-11-02 02:05:41,052 [INFO]: Data: b'2'      Children: ['c_0000000010', 'c_0000000011']
2023-11-02 02:06:17,667 [INFO]: '/election' children changed!
2023-11-02 02:06:17,668 [INFO]: I am the leader!
2023-11-02 02:06:17,674 [INFO]: Data: b'2'      Children: ['c_0000000011']
```