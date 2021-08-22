ARG NODE_VERSION=14
FROM node:$NODE_VERSION

# add more arguments from CI to the image so that `$ env` should reveal more info
ARG CI_BUILD_ID
ARG CI_BUILD_REF
ARG CI_REGISTRY_IMAGE
ARG CI_BUILD_TIME

ENV CI_BUILD_ID=$CI_BUILD_ID \
  CI_BUILD_REF=$CI_BUILD_REF \
  CI_REGISTRY_IMAGE=$CI_REGISTRY_IMAGE \
  CI_BUILD_TIME=$CI_BUILD_TIME

RUN yarn global add create-react-app && rm -rf $(yarn cache dir)
