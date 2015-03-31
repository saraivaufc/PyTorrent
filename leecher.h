#ifndef LEECHER_H
#define LEECHER_H
#include "piece.h"
#include <QList>

class Leecher : public Peer
{
public:
    Leecher();

private:
    QList<Piece> donwloaded_pieces;

};

#endif // LEECHER_H
