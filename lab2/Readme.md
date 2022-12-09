# Программа для поиска MTU до хоста
MTU (maximum transmission unit) - максимальный размер полезного блока данных одного пакета, который может быть передан протоколом без фрагментации. Для поиска MTU мы будем использовать бинарный поиск, подбирая размер таким образом, чтобы пакет пинга мог быть отправлен до хоста без фрагментации.

### Установка 
```bash
docker pull docker.io/library/ubuntu
docker build . -f Dockerfile -t mtu
```

### Запуск
###### Docker
```bash
docker run mtu <hostname>
```
##### Script help
```
usage: mtu.py [-h] [-v] host

Discover MTU to host.

positional arguments:
  host           host to determine MTU to

options:
  -h, --help     show this help message and exit
  -v, --verbose  print intermediate steps
```
### Пример
```
$ docker run mtu --verbose no_host?
Host name no_host? cannot be resolved
```
```
$ docker run mtu --verbose wiki.cs.hse.ru
Host wiki.cs.hse.ru is unreachable
```
```
$ docker run mtu --verbose ya.ru
Ping host# ya.ru with payload_size# 1000, returncode=0
Ping host# ya.ru with payload_size# 1500, returncode=1
Ping host# ya.ru with payload_size# 1250, returncode=0
Ping host# ya.ru with payload_size# 1375, returncode=0
Ping host# ya.ru with payload_size# 1437, returncode=0
Ping host# ya.ru with payload_size# 1468, returncode=0
Ping host# ya.ru with payload_size# 1484, returncode=1
Ping host# ya.ru with payload_size# 1476, returncode=1
Ping host# ya.ru with payload_size# 1472, returncode=0
Ping host# ya.ru with payload_size# 1474, returncode=1
Ping host# ya.ru with payload_size# 1473, returncode=1
MTU to host# ya.ru = 1472 bytes, packet size with headers = 1500 bytes
```