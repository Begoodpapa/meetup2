"* Setting *"	"* Value *"	"* Value *"	"* Value *"	"* Value *"	"* Value *"
Force Tags
Resource	resources/dmxmsg.tsv
suite setup	Connect To SUT Input Sync Env Setup
suite teardown	Disconnect From SUT

"* Variable *"	"* Value *"	"* Value *"	"* Value *"	"* Value *"	"* Value *"
${MAX TIME FOR CONNECT}	100
${PROCESSOR_ID_REGISTER}	dmxdaemon
${KERNEL_MODULE_INSEARTING_SCRIPT}	_TPL_PARA_KERNEL_MODULE_INSEARTING_SCRIPT_
@{NODE_LIST}	_TPL_PARA_NODES_
@{NODE_PROCESSOR_ID_LIST}	_TPL_PARA_PROCESSOR_ID_LIST_

"* Test Case *"	"* Action *"	"* Argument *"	"* Argument *"	"* Argument *"	"* Argument *"
Unload kernel module for every AS node	[Tags]	unload
	:for	${node}	in	@{NODE_LIST}
		execute cli	ssh ${node}
		Unload kernel module

Load kernel module for every AS node	[Tags]	load
	:for	${node}	in	@{NODE_LIST}
		execute cli	ssh ${node}
		Load kernel module

Register Processor ID for every node	[Tags]	reg_pid
	${list_len}	GetLength	${NODE_LIST}
	:for	${i}	in range	${list_len}
		execute cli	ssh ${NODE_LIST[${i}]}
		Register Processor ID	${NODE_PROCESSOR_ID_LIST[${i}]}

"* Keyword *"	"* Action *"	"* Argument *"	"* Argument *"	"* Argument *"	"* Argument *"
Connect To SUT Input Sync Env Setup
	Connect To SUT	${MAX TIME FOR CONNECT}
	Kill all dmx users for every node

Kill all dmx users for every node
	:for	${node}	in	@{NODE_LIST}
		execute cli	ssh ${node}
		execute cli	awk 'NR>1 {print $5}' /proc/dmxmsg/clients |xargs kill -9 |tee

Register Processor ID	[Arguments]	${pid}
	${rst}	execute cli	dmxcli2 -R ${pid}
	ShouldContain	${rst}	SUCCESS

Load kernel module
	${rst}	execute cli	${KERNEL_MODULE_INSEARTING_SCRIPT} start
	ShouldNotContain	${rst}	Invalid module format

Unload kernel module
	${rst}	execute cli	${KERNEL_MODULE_INSEARTING_SCRIPT} stop
	ShouldNotContain	${rst}	is in use


