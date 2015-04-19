import peer, tracker, address


def thread1():
	t = tracker.Tracker(address.Address("", 8000))
	t.run()
def thread2():
	p = peer.Peer(address.Address("127.0.0.1", 8022))
	p.run()

from threading import Thread

th=Thread( target=thread1, args = () )
th.start()


th2=Thread( target=thread2, args = () )
th2.start()