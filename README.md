[![Build Status](https://travis-ci.com/ONSdigital/census-rm-ops.svg?branch=master)](https://travis-ci.com/ONSdigital/census-rm-ops)
# Census RM Ops
Forked from [rasrm-ops](https://github.com/ONSdigital/rasrm-ops)
## Purpose
A utility tool to support the service operationally. This is intended for developers to use to support RM.

## Requirements
* Docker
* pipenv

## Installing dependencies
Run `make build`

## Building a docker image
Run `make docker`

## Running
1. Run `make docker-run`
1. Go to http://0.0.0.0:8003/

## Testing
Run `make test`

