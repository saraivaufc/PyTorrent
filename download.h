#ifndef DOWNLOAD_H
#define DOWNLOAD_H
#include <QTime>
#include <QString>

class Download
{
public:
    Download();


private:
    QTime start_time;
    int saving_diretory;
    float download_speed;
    QString pieces_downloaded;
    double download_size;

public:
    void pause();
    void start();

};

#endif // DOWNLOAD_H
