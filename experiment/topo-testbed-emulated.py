from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from time import sleep, time
from datetime import datetime

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/16')

    info( '*** Adding controllers\n' )
    c1=net.addController(name='c1',
                      controller=RemoteController,
                      ip='10.0.0.1',
                      protocol='tcp',
                      port=6653)
  
    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch, protocols='OpenFlow13')

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.11', mac='00:00:00:00:00:01', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.12', mac='00:00:00:00:00:02', defaultRoute=None)
    # h3 = net.addHost('h3', cls=Host, ip='10.0.0.13', mac='00:00:00:00:00:03', defaultRoute=None)
    # h4 = net.addHost('h4', cls=Host, ip='10.0.0.14', mac='00:00:00:00:00:04', defaultRoute=None)
    # h5 = net.addHost('h5', cls=Host, ip='10.0.0.15', mac='00:00:00:00:00:05', defaultRoute=None)
    # h6 = net.addHost('h6', cls=Host, ip='10.0.0.16', mac='00:00:00:00:00:06', defaultRoute=None)
    # h7 = net.addHost('h7', cls=Host, ip='10.0.0.17', mac='00:00:00:00:00:07', defaultRoute=None)
    # h8 = net.addHost('h8', cls=Host, ip='10.0.0.18', mac='00:00:00:00:00:08', defaultRoute=None)


    info( '*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s4)
    # net.addLink(h2, s1)

    # net.addLink(h3, s2)

    # net.addLink(h4, s2)

    # net.addLink(h5, s3)

    #net.addLink(h6, s4)
    #net.configLinkStatus( 'h6', 's4', 'down' )
    # net.addLink(h6, s3)
    #h6.nameToIntf['h6-eth1'].setIP('10.0.0.16/16')
    #h6.nameToIntf['h6-eth1'].setMAC('00:00:00:00:00:06')


    # net.addLink(h7, s4)

    #net.addLink(h8, s3)
    #net.configLinkStatus( 'h8', 's3', 'down' )
    # net.addLink(h8, s4)
    #h8.nameToIntf['h8-eth1'].setIP('10.0.0.18/16')
    #h8.nameToIntf['h8-eth1'].setMAC('00:00:00:00:00:08')

    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s1, s4)

    net.addLink(s2, s3)
    net.addLink(s2, s4)

    net.addLink(s3, s4)
    
    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        info(controller)
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c1])
    net.get('s2').start([c1])
    net.get('s3').start([c1])
    net.get('s4').start([c1])


    info( '*** Post configure switches and hosts\n')

    h1.cmd('sudo ./sv.o 80 000000000001 010CCD040001 4001 4001 MidiaCom1CFG/LLN0\$PhsMeas1 1 1 0 300 300 300 0 288 288 288 0 0 60 0 1 4 h1-eth0 &')

    # h2.cmd('sudo ./goose.o -i h2-eth0 -p 8081 &')
    # h3.cmd('sudo ./goose.o -i h3-eth0 -p 8080 &')
    sleep(5)

    # h2.cmd('sh scripts/h2pott.sh')
    # h3.cmd('sh scripts/h3pott.sh')
    # h3.cmd('sh scripts/h3dtt.sh')
    
    CLI(net)

    start = datetime.now()
    flag = True
    while True:
        print(datetime.now() - start)
        for index in ['1', '2', '3', '4']:
            c1.cmd('echo $(date) >> logs/s' + index + '.log')
            c1.cmd('sudo ovs-ofctl dump-flows s' + index +' -O OpenFlow13 >> logs/s' + index + '.log')
        sleep(1 * 60)
        if flag:
            net.configLinkStatus('s1', 's4', 'down')
        else:
            net.configLinkStatus('s1', 's4', 'up')
        flag = not flag
    
    # h2.cmd("tcpreplay -i h2-eth0 -K --loop 50000 goose_test.pcap &")
    # h1.cmd("wireshark -i h1-eth0 -Y arp &")
    # h2.cmd("wireshark -i h2-eth0 -Y arp &")
    # h3.cmd("wireshark -i h3-eth0 -Y arp &")
    # h4.cmd("wireshark -i h4-eth0 -Y arp &")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
