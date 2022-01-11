CryptoCurrency:

We have created a general purpose cryptocurrency here. We have also decentralised our blockchain for more realistic experience.

the Bainscoin.py file contains the general crpytocurrency code and can be used to deploy more nodes by changing the following options:

IN /mine_block function:
in line 109:
	bainschain.add_transaction(sender = node_address, reciever = '______', amt = 10)

The space can be used to add the name of the node.

and in the last line of the code
	app.run(host = '0.0.0.0', port = ____)

The space can be used to add port number for various nodes on the blockchain.


For the demo we have used:
- PORT 2001 - Rahul (node_2001)
- PORT 2002 - Sachin (node_2002)
- PORT 2003 - Bains (miner in this case) (node_2003)


And run them concurrently in three parallel consoles and checked it using postman.

The trials include:
- adding nodes to the network
- used replace chain to replace the chains and establish consensus
- add transanction to the node and mine the respective block
