"* Setting *"	"* Value *"	"* Value *"	"* Value *"	"* Value *"	"* Value *"
Force Tags	Product_Backlog_ID-B01050	_TPL_PARA_Iteration_ID	PRS-	owner-zhi-yuan.qin@nsn.com	element-IL	exec_type-automatic	type-FUT	release-IL1_RIS2	reviewer-xiaoping.wang.ext@nsn.com	rw-weekly	hw_env-RNC	ct-positive
Resource	resources/dmxmsg.tsv
suite setup	Connect To SUT	${MAX TIME FOR CONNECT}
suite teardown	Disconnect From SUT

"* Variable *"	"* Value *"	"* Value *"	"* Value *"	"* Value *"	"* Value *"
${PURE_SE_A}	_TPL_PARA_PURE_SE_A_ADDR_
${PURE_SE_B}	_TPL_PARA_PURE_SE_B_ADDR_
${6WIND_SE}	_TPL_PARA_6WIND_SE_ADDR_
${TIMEOUT}	30
${ 6WIND_SE_ F1&F2}	_TPL_PARA_6WIND_SE_F1nF2_
${PURE_SE_B F3&F4}	_TPL_PARA_PURE_SE_F3nF4_
${6WIND_SE &PURE_SE_A}	_TPL_PARA_6WIND_N_PURE_SE_A_
${PURE_SE_B&6WIND_SE}	_TPL_PARA_PURE_SE_B_N_6WIND_SE_
${6WIND_SE &6WIND_SE}	_TPL_PARA_6WIND_N_6WIND_SE_
${PURE_SE_A&PURE_SE_B}	_TPL_PARA_PURE_SE_B_N_PURE_SE_A_
${MAX TIME FOR CONNECT}	500

"* Test Case *"	"* Action *"	"* Argument *"	"* Argument *"	"* Argument *"	"* Argument *"
6.10 SE A send 10 dmxmsg (length 0) to SE B
	[Tags]	ATC_ID- DMXMSG.FUT.010.AT
	${out}	Use Dmxcli To Send Messages	${PURE_SE_A}	${PURE_SE_B}	10	0	1	0	0	${TIMEOUT}
	Should Contain	${out}	successful

6.11 SE A send 10 dmxmsg (length 65535-16) to SE B
	[Tags]	ATC_ID- DMXMSG.FUT.011.AT
	${out}	Use Dmxcli To Send Messages	${PURE_SE_A}	${PURE_SE_B}	1	1	10	65519	0	${TIMEOUT}
	Should Contain	${out}	successful

6.12 Pure SE A send 10 dmxmsg (no data) to 6WIND SE B
	[Tags]	ATC_ID- DMXMSG.FUT.012.AT
	${out}	Use Dmxcli To Send Messages	${PURE_SE_A}	${6WIND_SE}	10	0	1	0	0	${TIMEOUT}
	Should Contain	${out}	successful

6.13 Pure SE A send 10 dmxmsg (length 65535-16) to 6WIND SE B
	[Tags]	ATC_ID- DMXMSG.FUT.013.AT
	${out}	Use Dmxcli To Send Messages	${PURE_SE_A}	${6WIND_SE}	1	1	10	65519	0	${TIMEOUT}
	Should Contain	${out}	successful

6.14 6wind SE A send 10 dmxmsg (no data) to Pure SE B
	[Tags]	ATC_ID- DMXMSG.FUT.014.AT
	${out}	Use Dmxcli To Send Messages	${6WIND_SE}	${PURE_SE_B}	10	0	1	0	0	${TIMEOUT}
	Should Contain	${out}	successful

6.15 6wind SE A send 10 dmxmsg (65535) to Pure SE B
	[Tags]	ATC_ID- DMXMSG.FUT.015AT
	${out}	Use Dmxcli To Send Messages	${6WIND_SE}	${PURE_SE_B}	1	1	10	65519	1	${TIMEOUT}
	Should Contain	${out}	successful

6.16 Send No-Data Message from 6Win SE to Pure SE with different source and destionation family ID meanwhile
	[Tags]	ATC_ID- DMXMSG.FUT.016.AT
	${out}	Use Dmxcli To Send Messages	${ 6WIND_SE_ F1&F2}	${PURE_SE_B F3&F4}	1	1	10	0	1-1	${TIMEOUT}
	Should Contain	${out}	successful

6.17 Send largest Message from 6Win SE to Pure SE with different source and destionation family ID meanwhile
	[Tags]	ATC_ID- DMXMSG.FUT.017.AT
	${out}	Use Dmxcli To Send Messages	${ 6WIND_SE_ F1&F2}	${PURE_SE_B F3&F4}	1	1	10	65519	1-1	${TIMEOUT}
	Should Contain	${out}	successful

6.18 Send No-Data Message from 6Win SE to Pure SE with same source and different destionation family ID meanwhile
	[Tags]	ATC_ID- DMXMSG.FUT.018.AT
	${out}	Use Dmxcli To Send Messages	${6WIND_SE&6WIND_SE}	${PURE_SE_B F3&F4}	1	1	10	0	1-1	${TIMEOUT}
	Should Contain	${out}	successful

6.19 Send largest Message from 6Win SE to Pure SE with same source and different destionation family ID meanwhile
	[Tags]	ATC_ID- DMXMSG.FUT.019.AT
	${out}	Use Dmxcli To Send Messages	${6WIND_SE&6WIND_SE}	${PURE_SE_B F3&F4}	1	1	10	65519	1-1	${TIMEOUT}
	Should Contain	${out}	successful

6.20 Send no-data message from Pure SE B to 6Wind SE A, meanwhile Send no-data message from 6Wind SE A to Pure SE C
	[Tags]	ATC_ID- DMXMSG.FUT.020.AT
	${out}	Use Dmxcli To Send Messages	${PURE_SE_B&6WIND_SE}	${6WIND_SE &PURE_SE_A}	1	1	10	0	0-1	${TIMEOUT}
	Should Contain	${out}	successful

6.21 Send largest message from Pure SE B to 6Wind SE A, meanwhile Send largest message from 6Wind SE A to Pure SE C
	[Tags]	ATC_ID- DMXMSG.FUT.021.AT
	${out}	Use Dmxcli To Send Messages	${PURE_SE_B&6WIND_SE}	${6WIND_SE &PURE_SE_A}	1	1	10	65519	0-1	${TIMEOUT}
	Should Contain	${out}	successful

6.22 Send largest message from Pure SE B to 6Win SE A, meanwhile Send largest message from Pure SE C to 6Wind SE A.
	[Tags]	ATC_ID- DMXMSG.FUT.022.AT
	${out}	Use Dmxcli To Send Messages	${PURE_SE_A&PURE_SE_B}	${6WIND_SE &6WIND_SE}	1	1	10	65519	0-0	${TIMEOUT}
	Should Contain	${out}	successful


"* Keyword *"	"* Action *"	"* Argument *"	"* Argument *"	"* Argument *"	"* Argument *"

