#ifndef UPLOAD_H
#define UPLOAD_H
#include <QTime>

class Upload
{
public:
    Upload();
private:
    QTime start_time;
    float upload_speed;

public:
    void pause();
    void start();
};

#endif // UPLOAD_H
