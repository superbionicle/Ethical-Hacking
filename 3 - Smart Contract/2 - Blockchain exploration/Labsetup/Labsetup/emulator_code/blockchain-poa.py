#!/usr/bin/env python3
# encoding: utf-8

from seedemu import *
import os, sys

###############################################################################
emu = Emulator()

# Load the pre-built components and merge them
emu.load('./base-component.bin')


###############################################################################
# Create the Ethereum layer

eth = EthereumService()
blockchain = eth.createBlockchain(chainName="POA", consensus=ConsensusMechanism.POA)

# Create 10 accounts, each with 100 Ethers. We will use these accounts to
# generate background traffic (sending random transactions from them).
words = "great amazing fun seed lab protect network system security prevent attack future"
blockchain.setLocalAccountParameters(mnemonic=words, total=10, balance=100) 

# These 3 accounts are generated from the following phrase:
# "gentle always fun glass foster produce north tail security list example gain"
# They are for users. We will use them in MetaMask, as well as in our sample code.  
blockchain.addLocalAccount(address='0xF5406927254d2dA7F7c28A61191e3Ff1f2400fe9',
                           balance=30)
blockchain.addLocalAccount(address='0x2e2e3a61daC1A2056d9304F79C168cD16aAa88e9', 
                           balance=9999999)
blockchain.addLocalAccount(address='0xCBF1e330F0abD5c1ac979CF2B2B874cfD4902E24', 
                           balance=10)


# Create the Ethereum servers. 
asns  = [150, 151, 152, 153, 154, 160, 161, 162, 163, 164]
hosts_total = 2    # The number of servers per AS
signers  = []
i = 0
for asn in asns:
    for id in range(hosts_total):
        vnode = 'eth{}'.format(i)
        e = blockchain.createNode(vnode)

        displayName = 'Ethereum-POA-%.2d'
        e.enableGethHttp()  # Enable HTTP on all nodes
        e.unlockAccounts()
        if i%2  == 0:
            e.startMiner()
            signers.append(vnode)
            displayName = displayName + '-Signer'
            emu.getVirtualNode(vnode).appendClassName("Signer")
        if i%3 == 0:
            e.setBootNode(True)
            displayName = displayName + '-BootNode'
            emu.getVirtualNode(vnode).appendClassName("BootNode")

        emu.getVirtualNode(vnode).setDisplayName(displayName%(i))
        emu.addBinding(Binding(vnode, filter=Filter(asn=asn, nodeName='host_{}'.format(id))))
        i = i+1

# Add the Ethereum layer
emu.addLayer(eth)


#############################
# Create a new empty ethereum node for one of the tasks
# This node will use a pre-build image
newhost = emu.getLayer('Base').getAutonomousSystem(150).createHost('new_eth_node')
newhost.joinNetwork('net0')

# Add a pre-built image, and use it for New_Eth_Node
docker = Docker(internetMapEnabled=True, etherViewEnabled=True, platform=Platform.AMD64)
#docker = Docker(internetMapEnabled=True, etherViewEnabled=True, platform=Platform.ARM64)
image  = DockerImage(name='new_ethereum_node', dirName='./new_eth_node', local=True, software=[])
docker.addImage(image)
docker.setImageOverride(newhost, 'new_ethereum_node')

# Render and compile 
OUTPUTDIR = '../emulator'
emu.render()
emu.compile(docker, OUTPUTDIR, override = True)

# Copy the pre-build image to the output folder 
os.system('cp -r new_eth_node/ ' + OUTPUTDIR) 
