FROM caddy:2-builder AS builder

RUN xcaddy build --with github.com/corazawaf/coraza-caddy/v2

FROM caddy:2

#RUN mkdir /opt/wefrei_crs/
#COPY wewefrei_crs/* /opt/wefrei_crs

COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
