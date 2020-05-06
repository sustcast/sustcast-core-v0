FROM alpine
MAINTAINER kev <shuhan.mirza@gmail.com>

RUN apk add --no-cache ices
COPY data /etc/ices
COPY log /var/log/ices
COPY music /music
COPY playlist /playlist
CMD ["ices", "/etc/ices/ices.xml"]