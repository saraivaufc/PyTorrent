import peer, tracker, address

t = tracker.Tracker(address.Address("", 8000))
t.add_peer_in_swarm("sdadsadsa", "sijdijasid", peer.Peer( address.Address("127.0.0.1", 8022), [t,] ) ) 
t.run()