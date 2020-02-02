# DnsPod
ddns powerby DnsPod API

官方API使用规范 https://www.dnspod.cn/docs/info.html

官方API参考文档 https://www.dnspod.cn/docs/index.html

# install
1、Git clone 仓库，克隆的仓库压缩为压缩包，例如压缩为DnsPod.zip（也可以直接下载仓库压缩包）

2、然后```pip install DnsPod.zip```   这里的最后一个参数是压缩包文件路径

# usage

### ddns.py

ddns.py封装了一个DDNS类，直接调用可以简单地部署ddns服务，前提是域名是在腾讯云下或者DnsPod下
```python
>>> from DnsPod.ddns import DDNS
>>> inst = DDNS("example.com", "www")
>>> inst.run()
```
上述例子运行之后输入ID和Token，将创建为www.example.com创建一个A记录，记录为当前主机的公网ip，
第二个参数为子域名，是可选参数，若不传第二个参数，则创建example.com的A记录

### api.py

该文件实现了https://www.dnspod.cn/docs/records.html#record-list 中的部分api

- get_ip()
获取当前主机的公网ip
```python
>>> from DnsPod.api import get_ip
>>> get_ip()
106.127.136.112
```

- get_domain_id(yourdomain)
获取域名id

- add_record(domain, recordtype="A", subdomain="@", line="默认")
添加一条记录
```python
>>> from DnsPod.api import add_record
>>> record_id = add_record("example.com")
```
add_record添加记录成功的话返回所添加的记录ID，如果记录存在则返回None

- get_record_id(domain, subdomain="@", recordtype="A", line="默认")
获取记录id

- update(ip, domain, recordid, subdomain="@",  recordtype="A", line="默认", mx=None)
修改记录


