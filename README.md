# DnsPod
ddns powerby DnsPod API

# install
1、Git clone 仓库，克隆的仓库压缩为压缩包，例如压缩为DnsPod.zip（也可以直接下载仓库压缩包）

2、然后```pip install DnsPod.zip```   这里的最后一个参数是压缩包文件路径

# usage

### ddns.py

ddns.py封装了一个DDNS类，直接调用可以简单地部署ddns服务，前提是域名是在腾讯云下或者DnsPod下
```
>>> form DnsPod.ddns import DDNS
>>> inst = DDNS("example.com", "www")
>>> inst.run()
```
