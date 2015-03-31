#ifndef PIECE_H
#define PIECE_H
#include <QString>

class Piece
{
public:
    Piece();

private:
    long length;
    QString SHA1_hash_code;

public:
    void upload_piece();
    void download_piece();
};

#endif // PIECE_H
