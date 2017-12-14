#!/bin/bash

set -ev

if ! [[ "${TRAVIS_TAG}" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Tag is not a release one, not deploying."
    exit 0
fi

eval "$(ssh-agent -s)"
echo -e "${RESIN_DEPLOY_KEY}" > id_rsa
chmod 0600 id_rsa
ssh-add ./id_rsa
cat resinkey >> ~/.ssh/known_hosts
git remote add resin "${RESIN_REMOTE}"
git push resin master
