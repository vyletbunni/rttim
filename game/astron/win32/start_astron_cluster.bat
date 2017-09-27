@echo off
title Astron Service
cd ..
astrond --loglevel info config/cluster.yml

pause