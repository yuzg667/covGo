FROM centos:7.9.2009
MAINTAINER phonecom<yuzg667@126.com>
RUN yum clean all
RUN yum makecache fast
RUN yum -y install wget
RUN yum install -y deltarpm
# 安装python3 pip3 git
RUN yum -y update && yum -y install epel-release --nogpgcheck
RUN yum install python3-devel python3-pip -y
RUN yum install git -y
RUN yum install supervisor -y
RUN mkdir -p /home/workspace/covGo
RUN mkdir -p /usr/local/bin/

# 复制当前文件夹
COPY supervisord.conf /etc/supervisord.conf
COPY ./  /home/workspace/covGo/
RUN chmod 777 /home/workspace
RUN chmod 777 /home/workspace/*
RUN pip3 install -r /home/workspace/covGo/requirements.txt -i https://pypi.douban.com/simple

COPY ./cmdTools/goc /usr/local/bin/
RUN chmod 777 /usr/local/bin/*

# 安装go
RUN sh ./home/workspace/covGo/goinstall.sh
#修改go配置代理
RUN export PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin:/root/bin:/root/.go/bin
RUN source /root/.bashrc
RUN source /etc/profile
#RUN go env -w GOPROXY=https://goproxy.cn,direct

WORKDIR /home/workspace/covGo
EXPOSE 8899 7777
RUN chmod +x /home/workspace/covGo/run.sh

CMD ["/usr/bin/supervisord"]

