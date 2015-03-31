#ifndef SWARM_H
#define SWARM_H
#include "piece.h"
#include "peer.h"
#include <QList>

class Swarm
{
public:
    Swarm();
    void connect_to_peer();
    void disconnect_from_peer();
    void connect_to_all_peers_in_swarm();
    void disconnect_from_all_peers();
    QList<Peer> find_peers_with_piece(Piece piece);
    void add_peer_to_list(Peer peer);
    void remove_peer_from_list(Peer peer);
    QList<Peer> get_peers_with_highest_upload();
    void get_piece_from_peer(Piece piece, Peer peer);
};

#endif // SWARM_H
