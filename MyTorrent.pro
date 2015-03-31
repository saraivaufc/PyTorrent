TEMPLATE = app

QT += qml quick

SOURCES += main.cpp \
    peer.cpp \
    leecher.cpp \
    seeder.cpp \
    piece.cpp \
    swarm.cpp \
    torrent.cpp \
    file.cpp \
    tracker.cpp \
    download.cpp \
    upload.cpp \
    client.cpp

RESOURCES += qml.qrc

# Additional import path used to resolve QML modules in Qt Creator's code model
QML_IMPORT_PATH =

# Default rules for deployment.
include(deployment.pri)

HEADERS += \
    peer.h \
    leecher.h \
    seeder.h \
    piece.h \
    swarm.h \
    torrent.h \
    file.h \
    tracker.h \
    download.h \
    upload.h \
    client.h
