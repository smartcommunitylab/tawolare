FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:ubuntugis/ubuntugis-unstable
RUN apt-get install -y spatialite-bin
RUN apt-get install -y libpython2.7-dev
RUN apt-get install -y python-pysqlite2
RUN apt-get install -y git && \
	git clone https://github.com/smartcommunitylab/tawolare.git
RUN apt-get install -y wget && \
	apt-get install -y unzip

WORKDIR tawolare

RUN apt-get update && \
	apt-get install -y libjpeg8-dev && \
	apt-get install -y zlib1g-dev && \
	apt-get install -y libsqlite3-dev
RUN apt install -y python-pip && \
	pip install -r requirements.txt
RUN apt-get install -y libsqlite3-mod-spatialite && \
	cp ../usr/lib/x86_64-linux-gnu/mod_spatialite* .

RUN chmod +x setup_catasto.sh && \
	./setup_catasto.sh
RUN wget https://codeload.github.com/biggora/bootstrap-ajax-typeahead/zip/master && \
	mkdir typeahead && \
	unzip master -d ./typeahead/ && \
	rm master && \
	cp typeahead/bootstrap-ajax-typeahead-master/js/bootstrap* www/js && \
	rm -rf typeahead

EXPOSE 8515

CMD ["python", "tawolare.py"]