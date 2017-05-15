FROM quay.io/coreos/awscli

ENV HOME=/home
#    SOURCE_GROUP='' \
#    SOURCE_ROLE='' \

ADD . ${HOME}/
WORKDIR ${HOME}
RUN pip install ./dist/iamauth.tar.gz

CMD authorizedkeys -q list -g $SOURCE_GROUP -r $SOURCE_ROLE -f value -c SSHPublicKeyBody


