"* Setting *"	"* Value *"	"* Value *"	"* Value *"	"* Value *"	"* Value *"
Force Tags	_TPL_PARA_Product_Backlog_ID	_TPL_PARA_Iteration_ID	PRS-	owner-zhi-yuan.qin@nsn.com	element-IL	exec_type-automatic	type-FUT	release-IL1_RIS2	reviewer-xiaoping.wang.ext@nsn.com	rw-weekly	hw_env-RNC	ct-positive
...	QL-0
Resource	resources/dmxmsg.tsv
suite setup	Connect To SUT	${MAX TIME FOR CONNECT}
suite teardown	Disconnect From SUT

"* Variable *"	"* Value *"	"* Value *"	"* Value *"	"* Value *"	"* Value *"
${TIMEOUT}	30
${DAEMON}	5002:AD9C:0
${SE}	_TPL_PARA_SE_ADDR
${MULTI_SE}	_TPL_PARA_MULTI_SE_ADDR
${MULTI_DAEMON}	_TPL_PARA_MULTI_DAEMON_ADDR
${SINGLE_SE}	_TPL_PARA_SINGLE_SE_ADDR
${SINGLE_DAEMON}	5002:AD9C:0-5002:AD9C:0
${MAX TIME FOR CONNECT}	50

"* Test Case *"	"* Action *"	"* Argument *"	"* Argument *"	"* Argument *"	"* Argument *"
6.1 Send Ten Short Message from LINUX to SE
	[Tags]	ATC_ID- DMXMSG.FUT.001.AT
	${out}	Use Dmxcli To Send Messages	${DAEMON}	${SE}	10	0	1	100	1	${TIMEOUT}
	Should Contain	${out}	successful

6.2 Send Ten Short Message from LINUX to SE with Different Destination Family Id
	[Tags]	ATC_ID- DMXMSG.FUT.002.AT
	${out}	Use Dmxcli To Send Messages	${SINGLE_DAEMON}	${MULTI_SE}	10	0	1	100	1-1	${TIMEOUT}
	Should Contain	${out}	successful

6.3 Send Ten Short Message From SE To Linux
	[Tags]	ATC_ID- DMXMSG.FUT.003.AT
	${out}	Use Dmxcli To Send Messages	${SE}	${DAEMON}	10	0	1	100	0	${TIMEOUT}
	Should Contain	${out}	successful

6.4 Send Ten Short Message from SE to Different LINUX Daemon
	[Tags]	ATC_ID- DMXMSG.FUT.004.AT
	${out}	Use Dmxcli To Send Messages	${SINGLE_SE}	${MULTI_DAEMON}	10	0	1	100	0-0	${TIMEOUT}
	Should Contain	${out}	successful

6.5 Send Ten Largest Message from LINUX to SE
	[Tags]	ATC_ID- DMXMSG.FUT.005.AT
	${out}	Use Dmxcli To Send Messages	${DAEMON}	${SE}	10	0	1	65519	1	${TIMEOUT}
	Should Contain	${out}	successful

6.6 Send Ten Largest Message from LINUX to SE with Different Destination Family Id
	[Tags]	ATC_ID- DMXMSG.FUT.006.AT
	${out}	Use Dmxcli To Send Messages	${SINGLE_DAEMON}	${MULTI_SE}	10	0	1	65519	1-1	${TIMEOUT}
	Should Contain	${out}	successful

6.7 Send Ten Largest Message From SE To Linux
	[Tags]	ATC_ID- DMXMSG.FUT.007.AT
	${out}	Use Dmxcli To Send Messages	${SE}	${DAEMON}	10	0	1	65519	0	${TIMEOUT}
	Should Contain	${out}	successful

6.8 Send Ten Largest Message from SE to Different LINUX Daemon
	[Tags]	ATC_ID- DMXMSG.FUT.008.AT
	${out}	Use Dmxcli To Send Messages	${SINGLE_SE}	${MULTI_DAEMON}	10	0	1	65519	0-0	${TIMEOUT}
	Should Contain	${out}	successful

6.9 Send No-data Message from LINUX to SE
	[Tags]	ATC_ID- DMXMSG.FUT.009.AT
	${out}	Use Dmxcli To Send Messages	${DAEMON}	${SE}	10	0	1	0	1	${TIMEOUT}
	Should Contain	${out}	successful


"* Keyword *"	"* Action *"	"* Argument *"	"* Argument *"	"* Argument *"	"* Argument *"

