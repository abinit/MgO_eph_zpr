#!/bin/bash
cd /Users/gmatteo/git_repos/MgO_eph_zpr/flow_zpr_mgo/w1/outdata
# OpenMp Environment
export OMP_NUM_THREADS=1
# Commands before execution
ulimit -n 2048
source ~/env.sh
export PATH=$HOME/git_repos/abinit/_build/src/98_main:$PATH

mpirun  -n 1 mrgddb --nostrict < /Users/gmatteo/git_repos/MgO_eph_zpr/flow_zpr_mgo/w1/outdata/mrgddb.stdin > /Users/gmatteo/git_repos/MgO_eph_zpr/flow_zpr_mgo/w1/outdata/mrgddb.stdout 2> /Users/gmatteo/git_repos/MgO_eph_zpr/flow_zpr_mgo/w1/outdata/mrgddb.stderr
