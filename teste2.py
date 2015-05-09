import peer, tracker, address

p = peer.Peer(address.Address("127.0.0.1", 45999), [ tracker.Tracker( address.Address("localhost", 50000)), ])
p.run()
#p.upload("API_siconv_140515.sql")
#p.upload("Raimundos  mulher de fases.mp3")
p.upload('teste.txt')
#p.download("Raimundos  mulher de fases.mp3.pytorrent")