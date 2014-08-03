package com.puncsky.SecureCSI;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class Items implements Iterable<List<byte []>> {
    private ArrayList<List<byte []>> _base;
    private int _currentSize = 0;

    public Items(int countOfNodes) {
        _base = new ArrayList<List<byte []>>(countOfNodes);
        for (int i = 0; i < countOfNodes; i++) {
            _base.add(null);
        }
    }

    public void Set(int nodeID, List<byte []> items) {
        if (_base.get(nodeID) == null) {
            _currentSize ++;
        }
        _base.set(nodeID, items);
        LOG.Debug("ItemsCollect size increased to " + _currentSize + ".");
    }

    public List<byte []> Get(int nodeID) {
        return _base.get(nodeID);
    }

    public boolean IsFull() {
        return _currentSize == _base.size();
    }

    @Override
    public Iterator<List<byte[]>> iterator() {
        return _base.iterator();
    }
}
