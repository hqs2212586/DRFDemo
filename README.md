# rest-framework框架——版本控制流程示例

## 一、


## 一、数据结构设计和生成

模型文件所在目录：MadKing/assets/models.py

执行数据迁移：
```bash
(python37) bash-3.2$ python manage.py makemigrations
(python37) bash-3.2$ python manage.py migrate
```

创建admin用户：
```bash
(python37) bash-3.2$ python manage.py createsuperuser
Username (leave blank to use 'hqs'): hqs
Email address: 
Password: 
Password (again): 
Error: Blank passwords aren't allowed.   # 密码不能为空
Password: 
Password (again): 
This password is too short. It must contain at least 8 characters.   # 密码过于简单可强制同意
This password is too common.
This password is entirely numeric.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```

## 二、CMDB客户端
http协议发送agent节点信息。
客户端代码存放地址：MadKing/MadkingClient

### 1、客户端子目录介绍
bin：入口程序
conf：配置
core：代码
logs：日志
plugins：插件
var：

### 2、python安装wmi模块
微软官网对WMI的介绍：
[WMI官网介绍](https://docs.microsoft.com/zh-cn/windows/desktop/WmiSdk/wmi-start-page)

WMI的全称是Windows Management Instrumentation，即Windows管理规范。
它是Windows操作系统上管理数据和操作的基础设施。我们可以使用WMI脚本或者应用自动化管理任务等。

WMI并不原生支持Python。不过没有关系，它支持VB，而Python中的两个第三方库wmi和win32com，均能以类似VB的用法来使用。

### 3、linux客户端收集数据并发送

```bash
[root@MiWiFi-R4C-srv bin]# python NedStark.py collect_data

[root@MiWiFi-R4C-srv bin]# python NedStark.py report_asset
token format:[hqs@qq.com
1546107460
hqs123]
token :[a0e96c23abae886cca8bec533a50f034]
Connecting [http://192.168.31.28:8000/asset/report/asset_with_no_asset_id/?user=hqs@qq.com&timestamp=1546107460&token=ae886cc], it may take a minute
[post]:[http://192.168.31.28:8000/asset/report/asset_with_no_asset_id/?user=hqs@qq.com&timestamp=1546107460&token=ae886cc] response:
{u'needs_aproval': u"this is a new asset,needs IT admin's approval to create the new asset id."}
```

## 三、服务端解析
### 1、


### 2、API安全认证
主要用于解决server端和client端数据通信时，数据被第三方截取的问题。
用户名和时间戳明文发给服务器端，密码转为md5值发送。
服务器端根据用户名在数据库查到password，然后根据username、password、时间戳求出md5值与客户端发送的md5值作比对。
使用redis和membercache保存验证成功的登录信息，其他访问链接通过同样的md5值、用户名、时间戳想登录，直接被拒绝。


### 3、restful api设计
越来越多的人开始意识到，网站即软件，而且是一种新型的软件。

这种"互联网软件"采用客户端/服务器模式，建立在分布式体系上，通过互联网通信，具有高延时（high latency）、高并发等特点。

网站开发，完全可以采用软件开发的模式。

![RESTful架构](http://www.ruanyifeng.com/blogimg/asset/201109/bg2011091202.jpg)

RESTful架构，就是目前最流行的一种互联网软件架构。它结构清晰、符合标准、易于理解、扩展方便，所以正得到越来越多网站的采用。

#### (1)名称
Fielding将他对互联网软件的架构原则，定名为REST，即 ``Representational State Transfer`` 的缩写。我对这个词组的翻译是"表现层状态转化"。

如果一个架构符合REST原则，就称它为RESTful架构。

#### (2)资源
REST的名称"表现层状态转化"中，省略了主语。"表现层"其实指的是"资源"（Resources）的"表现层"。

所谓"资源"，就是网络上的一个实体，或者说是网络上的一个具体信息。它可以是一段文本、一张图片、一首歌曲、一种服务，总之就是一个具体的实在。你可以用一个URI（统一资源定位符）指向它，每种资源对应一个特定的URI。要获取这个资源，访问它的URI就可以，因此URI就成了每一个资源的地址或独一无二的识别符。

所谓"上网"，就是与互联网上一系列的"资源"互动，调用它的URI。

#### (3)表现层
"资源"是一种信息实体，它可以有多种外在表现形式。我们把"资源"具体呈现出来的形式，叫做它的"表现层"（Representation）。

比如，文本可以用txt格式表现，也可以用HTML格式、XML格式、JSON格式表现，甚至可以采用二进制格式；图片可以用JPG格式表现，也可以用PNG格式表现。

URI只代表资源的实体，不代表它的形式。严格地说，有些网址最后的".html"后缀名是不必要的，因为这个后缀名表示格式，属于"表现层"范畴，而URI应该只代表"资源"的位置。它的具体表现形式，应该在HTTP请求的头信息中用Accept和Content-Type字段指定，这两个字段才是对"表现层"的描述。

#### (4)状态转化
访问一个网站，就代表了客户端和服务器的一个互动过程。在这个过程中，势必涉及到数据和状态的变化。

互联网通信协议HTTP协议，是一个**无状态协议**。这意味着，所有的状态都保存在服务器端。因此，如果客户端想要操作服务器，必须通过某种手段，让服务器端发 ``状态转化（State Transfer）``。而这种转化是建立在表现层之上的，所以就是"表现层状态转化"。

客户端用到的手段，只能是HTTP协议。具体来说，就是HTTP协议里面，四个表示操作方式的动词：GET、POST、PUT、DELETE。它们分别对应四种基本操作：GET用来获取资源，POST用来新建资源（也可以用于更新资源），PUT用来更新资源，DELETE用来删除资源。

#### (5)综述

综合上面的解释，我们总结一下什么是RESTful架构：

1. 每一个URI代表一种资源；

2. 客户端和服务器之间，传递这种资源的某种表现层；

3. 客户端通过四个HTTP动词，对服务器端资源进行操作，实现"表现层状态转化"。

### 4、URI和URL的区别
URI，是uniform resource identifier，统一资源标识符，用来唯一的标识一个资源。而URL是uniform resource locator，统一资源定位器，它是一种具体的URI，即URL可以用来标识一个资源，而且还指明了如何locate这个资源。

[URI和URL的区别](http://www.cnblogs.com/gaojing/archive/2012/02/04/2413626.html)