#ifndef PEER_H
#define PEER_H

#include <QObject>
#include <QString>
#include "piece.h"

class Peer : public QObject
{
    Q_OBJECT
public:
    explicit Peer(QObject *parent = 0);

private:
    long ip_address;
    QString client_code;
    double upload_bandwith;
    double download_bandwith;


public:
    void get_piece(Piece piece);

signals:

public slots:

};

#endif // PEER_H
