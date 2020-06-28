#!/bin/bash

make build
make HTTP_PORT=$HTTP_PORT run
