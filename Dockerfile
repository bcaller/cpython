FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive

RUN sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list && \
  apt-get update && \
  apt-get build-dep -y python3.9 && \
  rm -rf /var/lib/apt/lists/*

COPY Grammar /src/Grammar
COPY Include /src/Include
COPY Lib /src/Lib
COPY Misc /src/Misc
COPY Modules /src/Modules
COPY Objects /src/Objects
COPY Parser /src/Parser
COPY PC /src/PC
COPY PCbuild /src/PCbuild
COPY Programs /src/Programs
COPY Python /src/Python
COPY Tools /src/Tools
COPY aclocal.m4 config.guess config.sub configure configure.ac install-sh Makefile.pre.in pyconfig.h.in setup.py /src/
WORKDIR /src/

RUN ./configure && make -s -j2 > /dev/null

COPY spit.py /src/
