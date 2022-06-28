# covGo

GO语言的覆盖率平台


## 环境要求
系统：linux、mac（不支持windows）
Go: 1.13+
python: 3.6+

## 安装
### coGo服务端安装
1、安装GOC
```
# Mac/AMD64
curl -s -L "https://github.com/qiniu/goc/releases/latest" | sed -nE 's!.*"([^"]*-darwin-amd64.tar.gz)".*!https://github.com\1!p' | xargs -n 1 curl -L  | tar -zx && chmod +x goc && mv goc /usr/local/bin

# Linux/AMD64
curl -s -L "https://github.com/qiniu/goc/releases/latest" | sed -nE 's!.*"([^"]*-linux-amd64.tar.gz)".*!https://github.com\1!p' | xargs -n 1 curl -L  | tar -zx && chmod +x goc && mv goc /usr/local/bin

# Linux/386
curl -s -L "https://github.com/qiniu/goc/releases/latest" | sed -nE 's!.*"([^"]*-linux-386.tar.gz)".*!https://github.com\1!p' | xargs -n 1 curl -L  | tar -zx && chmod +x goc && mv goc /usr/local/bin

```
安装后命令行输入goc，查看是否有效。

2、安装gocov、gocov-xml、gocov-html
```
go install github.com/axw/gocov/gocov@latest
go install github.com/AlekSi/gocov-xml@latest
go install github.com/matm/gocov-html@latest
```
安装后命令行输入gocov、gocov-xml、gocov-html查看是否有效。
### 被测服务器安装
只需要安装goc，安装方法同上

## 运行
#### covGo所在服务器开启
假设covGo所在服务器ip为10.20.8.21
1、covGo服务
安装依赖：`pip install -r requirements.txt`
运行：`python3 manage.py runserver 0.0.0.0:8000`

2、 开启goc服务
```goc server```  默认端口为7777
#### 被测服务器（一般指go后端服务器）开启
进入go项目的根目录，使用goc编译打包：
```
goc build --center=http://10.20.8.21:7777 --agentport=:46599
```
备注：`--center=`的值为goc服务ip端口； `--agentport=`的值为被测服务外露的端口


## 使用
covGo平台页面
1、新建项目
2、覆盖率任务


## Related tools and services

[goc](https://github.com/qiniu/goc):
goc is a comprehensive coverage testing system for The Go Programming Language, especially for some complex scenarios, like system testing code coverage collection and accurate testing.

[gocov](https://github.com/axw/gocov):
Coverage reporting tool for The Go Programming Language

[gocov-html](https://github.com/matm/gocov-html):
A simple helper tool for generating HTML output from gocov.

[gocov-xml](https://github.com/AlekSi/gocov-xml):
A simple helper tool for generating XML output in Cobertura format for CIs like Jenkins and others from gocov. 
