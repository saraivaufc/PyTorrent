#ifndef TORRENT_H
#define TORRENT_H
#include <QString>
#include <QList>

#include "file.h"
#include "piece.h"

class Torrent
{
public:
    Torrent();

private:
    QString tracker_url;
    QList<File> file_list;
    QString info_hash_code;

public:
    void remove_torrent();
    QList<Piece> get_pieces();
};

#endif // TORRENT_H
