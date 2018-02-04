ipbr_id=100
echo "<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE raml SYSTEM "raml21.dtd">
<raml xmlns='raml21.xsd' version='2.1'>
        <cmData type='actual'>
                <header>
                        <log dateTime='2010-03-24T06:53:45Z' action='created' user='SKOIVU'>
                                IP Plan file
                        </log>
                </header>"
for((i=10;i<=19;i++));
do
  for((j=100;j<=109;j++));
  do 
       echo "
       <managedObject class='ADDR' version='mcRN3.0' operation='create' distName='RNC-02/IP-1/OWNER-QNUP-0/ADDR-191.251.10.$i-ethtest20'>
            <p name='mask'>24</p>
       </managedObject>
       
       <managedObject class='ADDR' version='mcRN3.0' operation='create' distName='RNC-02/IP-1/OWNER-QNUP-2/ADDR-191.251.10.$j-ethtest20'>
            <p name='mask'>24</p>
       </managedObject>
       
       <managedObject class='BFDS' version='mcRN3.0' operation='create' distName='RNC-02/IP-1/OWNER-QNUP-0/BFDS-Flash-$ipbr_id'>
            <p name='vrf'>default</p>
            <p name='srcAddr'>191.251.10.$i</p>
            <p name='dstAddr'>191.251.10.$j</p>
            <p name='rxInterval'>250</p>
            <p name='txInterval'>250</p>
            <p name='referenceId'>$ipbr_id</p>
        </managedObject>
        
        <managedObject class='BFDS' version='mcRN3.0' operation='create' distName='RNC-02/IP-1/OWNER-QNUP-2/BFDS-Flash-$ipbr_id'>
            <p name='vrf'>default</p>
            <p name='srcAddr'>191.251.10.$j</p>
            <p name='dstAddr'>191.251.10.$i</p>
            <p name='rxInterval'>250</p>
            <p name='txInterval'>250</p>
            <p name='referenceId'>0</p>
        </managedObject>
        "      
ipbr_id=$(($ipbr_id+1));
   done;
done;
echo "
	</cmData>
</raml>"
