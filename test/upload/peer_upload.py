#-*- encode=utf-8 -*-

import torrent

peer_download = torrent.Peer(torrent.Address("127.0.0.1",50002), [torrent.Tracker(torrent.Address("127.0.0.1", 50000))])
peer_download.run()

peer_download.upload("musica.mp3")
#peer_download.upload("music.ape")