import torrent

print "Server Start"

server = torrent.Tracker(torrent.Address("127.0.0.1", 50000))
server.run()
