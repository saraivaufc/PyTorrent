#ifndef TRACKER_H
#define TRACKER_H
#include <QString>

#include "torrent.h"
#include "swarm.h"

class Tracker
{
public:
    Tracker();

private:
    QString url;

public:
    Swarm get_peer_list(Torrent torrent);
};

#endif // TRACKER_H
