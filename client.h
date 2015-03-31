#ifndef CLIENT_H
#define CLIENT_H
#include <QString>
#include <QList>

#include "torrent.h"
#include "peer.h"


class Client
{
public:
    Client();

private:
    QString client_code;
    long ip_address;
    double upload_bandwith;
    double download_bandwith;
    QString saving_diretory;

public:
    void open_torrent(Torrent torrent);
    void new_download(Torrent torrent, QList<Peer> peer_list);
    void new_upload(Torrent torrent, QList<Peer> peer_list);
    void connect_to_tracker(QString tracker_url);
    void connect_to_peer(Peer peer);
    void reaquest_torrent_pieces(Torrent torrent);
};

#endif // CLIENT_H
