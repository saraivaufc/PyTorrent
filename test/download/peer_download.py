#-*- encode=utf-8 -*-

import torrent

peer_download = torrent.Peer(torrent.Address("127.0.0.1",50001), [torrent.Tracker(torrent.Address("127.0.0.1", 50000))])
peer_download.run()

#peer_download.download("musica.mp3.pytorrent")
peer_download.download("music.ape.pytorrent")
#peer_download.upload("music.ape.pytorrent")