import peer, tracker, address

p = peer.Peer(address.Address("127.0.0.1", 50123), [ tracker.Tracker( address.Address("localhost", 50000)), ])
p.run()
#p.upload("Raimundos  mulher de fases.mp3")
p.download("Raimundos  mulher de fases.mp3.pytorrent")