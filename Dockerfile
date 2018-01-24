FROM d87904488/ubuntu-cn

RUN apt update && \
	apt install -y python && \
	apt install -y python3 && \
	apt install -y  openjdk-8-jre && \
	apt install -y  openjdk-8-jdk && \
	apt install -y  cmake && \
	apt install -y  gcc && \
	apt install -y  g++ && \
	apt install -y  python3-pip && \
	apt install -y  libseccomp-dev && \
	apt install -y  git && \
	pip3 install --no-cache-dir flask gunicorn gevent virtualenv && \
	cd /usr && \
	git clone https://github.com/Eagle-OJ/eagle-oj-judger.git --depth=1 && \
	cd eagle-oj-judger && \
	mkdir build && \
	cd build && \
	cmake .. && \
	make && \
	make install && \
	cd ../bindings/Python && \
	python3 setup.py install && \
	cd /usr && \
	mkdir myenv && \
	cd myenv && \
	virtualenv --system-site-packages py3env && \
	cd py3env && source bin/activate && \
	python /usr/eagle-oj-judger/Judger/server/initEnv.py  && \
	apt clean && \
	apt autoremove && \
	rm -rf /var/lib/apt/lists/* && \
	useradd -u 1001 compiler
EXPOSE 5000