import peer, tracker, address

p = peer.Peer(address.Address("127.0.0.1", 8022), [ tracker.Tracker( address.Address("127.0.0.1", 8000)), ])
#p.upload("Raimundos  mulher de fases.mp3")
p.download("Raimundos  mulher de fases.mp3.pytorrent")