FROM mcr.microsoft.com/iotedge/opc-plc:latest

WORKDIR /app

RUN mkdir -p /app/customized

COPY ./res/customized_node/ /app/customized/


RUN apt-get update && apt-get install -y \
    curl \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
#     CMD curl -f http://localhost:8080/pn.json || exit 1

CMD [ "--autoaccept","--pn=50000", "--sph", "--sn=5", "--sr=10", "--st=uint", "--fn=5", "--fr=1", "--ft=uint", "--gn=5", "--ll=debug", "--ph=opcplc", "--cdn=opcplc", "--ap=/app/pki/", "--nodesfile=/app/customized/node.json"]