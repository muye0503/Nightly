#!/bin/bash

testSpin=$1
mefaHost=$(hostname);
echo $mefaHost;

timeStamp=$(date +%y_%m_%d_%H_%M);
echo $timeStamp;


mefaPlat=/Jenkins/workspace/20-Vx7_Nig/vxworks_7/mefa_platform
suiteDir=/Jenkins/workspace/20-Vx7_Nig/vxworks_7/mefa_cases/features
dockerDNS="-3rdserver -dontdestorybridge"
#buildOps="-dontcopyhosttool -nobuild -tests 4.0"
buildOps="-tests 4.0,4.1"
#buildOps="-dontcopyhosttool -nobuild"
#buildOps=""
#buildOps="-dontcopyhosttool -nobuild -tests 4.0,4.1"

#dvdPath="/buildarea1/yliu2/$testSpin -buildserver target:vxTarget@128.224.179.60"
#dvdPath="/mydisk/$testSpin -buildserver windriver:windriver@128.224.167.34"
dvdPath="/net/pek-vx-system1/buildarea1/yliu2/nightly/$testSpin"

testSuite="VXSMP";

cd $mefaPlat;

 
# Q35 
#for testSuite in $sanity; do
./runTest.tcl -suite $testSuite -suitedir $suiteDir -path $dvdPath -vxworks 7 -syslog 3 -caselog 2 -productinclude 6.9.2.f0 $dockerDNS $buildOps \
-64bit -target cpu=NEHALEM,bsp=itl_generic,tool=llvm,portSrv=128.224.164.51:2012,pduSrv=128.224.164.166:8,bootdev=gei5,eif=eth1,ftp=windriver,passwd=windriver \
-fastvsb -buildcfgfile build_q35_vx7_smp_4.cfg -performance
