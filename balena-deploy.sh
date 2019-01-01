#!/bin/bash

set -ev

eval "$(ssh-agent -s)"
echo -e "${BALENA_DEPLOY_KEY}" > id_rsa
chmod 0600 id_rsa
ssh-add ./id_rsa
cat balenakeys >> ~/.ssh/known_hosts
git remote add balena "${BALENA_REMOTE}"
git push balena master
