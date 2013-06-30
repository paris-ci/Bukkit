#!/bin/sh

cd "$( dirname "$0" )"
curl -sS https://github.com/paris-ci/Bukkit/archive/master.zip > master.zip && \
unzip master.zip                                  && \
rm master.zip