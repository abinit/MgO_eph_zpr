#!/bin/bash

for td in {0..30}; do
    #ls new_flow_zpr_mgo/w1/t${td}/outdata/out_DEN*
    cp new_flow_zpr_mgo/w1/t${td}/outdata/out_DEN*  flow_zpr_mgo/w1/t${td}/outdata/
done
