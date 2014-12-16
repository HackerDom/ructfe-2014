#!/bin/bash

mplayer -rawaudio samplesize=2:channels=1:rate=16000 -demuxer rawaudio $1

