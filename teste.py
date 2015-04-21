import peer, tracker, address

t = tracker.Tracker(address.Address("127.0.0.1", 50000))
t.run()