FROM node:18-alpine AS base

FROM base AS base-deps
WORKDIR /app

COPY --link ./yarn.lock ./package.json ./.yarnrc.yml ./

FROM base AS installer
WORKDIR /app

COPY --link --from=base-deps /app/package.json ./package.json
COPY --link --from=base-deps /app/yarn.lock ./yarn.lock
COPY --link .yarnrc.yml .
RUN yarn install

FROM base AS builder
WORKDIR /app

COPY --link --from=installer /app .
COPY --link tsconfig.json tsconfig.json
RUN yarn build

FROM base AS development
WORKDIR /app

COPY --link --from=installer /app .

ENV NODE_ENV=development

CMD ["yarn", "dev"]
