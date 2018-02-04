"* Setting *"	"* Value *"	"* Value *"	"* Value *"	"* Value *"	"* Value *"
Suite Setup	Connect To SUT	${MAX TIME FOR CONNECT}
Suite Teardown	Disconnect From SUT
Force Tags	Product_Backlog_ID-B01050	Iteration_ID-I00668	PRS-	owner-zhi-yuan.qin@nsn.com	element-IL	exec_type-automatic	type-FUT	release-IL1_RIS2	reviewer-xiaoping.wang.ext@nsn.com	rw-weekly	hw_env-RNC	ct-positive
Resource	resources/dmxmsg.tsv

"* Variable *"	"* Value *"	"* Value *"	"* Value *"	"* Value *"	"* Value *"
${PURE_SE_A}	_TPL_PARA_PURE_SE_A_ADDR_
${6WIND_SE}	5B5D:457:0
${TIMEOUT}	30
${MAX TIME FOR CONNECT}	500

"* Test Case *"	"* Action *"	"* Argument *"	"* Argument *"	"* Argument *"	"* Argument *"
Pure SE A Send 10 Dmxmsg (no Data) To 6WIND SE B
	[Tags]	ATC_ID- DMXMSG.FUT.04.AT
	${out} =	Use Dmxcli To Send Messages	${PURE_SE_A}	${6WIND_SE}	10	0	1	0	0	${TIMEOUT}
	Should Contain	${out}	successful

Pure SE A Send 10 Short Dmxmsg To 6WIND SE B
	[Tags]	ATC_ID- DMXMSG.FUT.05.AT
	${out} =	Use Dmxcli To Send Messages	${PURE_SE_A}	${6WIND_SE}	10	0	1	100	0	${TIMEOUT}
	Should Contain	${out}	successful

Pure SE A Send 10 Dmxmsg (length 65535-16) To 6WIND SE B
	[Tags]	ATC_ID- DMXMSG.FUT.06.AT
	${out} =	Use Dmxcli To Send Messages	${PURE_SE_A}	${6WIND_SE}	1	0	10	30000	1	${TIMEOUT}
	Should Contain	${out}	successful


"* Keyword *"	"* Action *"	"* Argument *"	"* Argument *"	"* Argument *"	"* Argument *"

