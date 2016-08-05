#-*- encode=utf-8 -*-

import torrent

peer_download = torrent.Peer(torrent.Address("127.0.0.1",50007), [torrent.Tracker(torrent.Address("127.0.0.1", 50000))])
peer_download.run()

#peer_download.upload("music.ape")
peer_download.upload("toca.mp4")

peer_download2 = torrent.Peer(torrent.Address("127.0.0.1",50008), [torrent.Tracker(torrent.Address("127.0.0.1", 50000))])
peer_download2.run()

#peer_download2.upload("music.ape")
peer_download2.upload("toca.mp4")

peer_download3 = torrent.Peer(torrent.Address("127.0.0.1",50009), [torrent.Tracker(torrent.Address("127.0.0.1", 50000))])
peer_download3.run()

#peer_download3.upload("music.ape")
peer_download3.upload("toca.mp4")