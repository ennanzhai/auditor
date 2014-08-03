package com.puncsky.SecureCSI;

import javax.crypto.NoSuchPaddingException;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;
import java.util.Random;

public class Node {

    public final int NodeID;

    String[] _myItems;

    private int _countOfAllNodes;

    private Items _allItemsTable;

    private int[] _sharedItemsNumber;

    private InetSocketAddress[] _allAddresses;

    private TcpSocket _socket;

    public Node(int nodeID,
                String[] myItems,
                InetSocketAddress[] allAddresses) throws IOException {
        NodeID = nodeID;
        _myItems = myItems;
        _countOfAllNodes = allAddresses.length;
        _allItemsTable = new Items(_countOfAllNodes);
        _sharedItemsNumber = new int[_countOfAllNodes];
        _allAddresses = allAddresses;

        // Listen on the port.
        _socket = new TcpSocket(this, _allAddresses[NodeID]);
    }

    public void onRecvInProgress(int hopCount, List<byte[]> items)
            throws IOException,
            NoSuchProviderException,
            InvalidKeyException,
            NoSuchAlgorithmException,
            NoSuchPaddingException,
            InvalidAlgorithmParameterException {
        if (hopCount < _countOfAllNodes) {
            // The message is still in progress.
            encryptAndShuffle(items);
            _socket.send(items,
                         hopCount + 1,
                         _allAddresses[(NodeID + 1) % _countOfAllNodes],
                         Message.InProgress);
        } else if (hopCount == _countOfAllNodes) {
            // The message has traveled through the entire circle.
            _allItemsTable.Set(NodeID, items);
            _socket.BroadCast(items, _allAddresses);
            if (_allItemsTable.IsFull()) {
                calcSharedItems();
            }
        }
    }

    public void onRecvAllEncrypted(int sourceNodeID, List<byte[]> items) {
        _allItemsTable.Set(sourceNodeID, items);
        if (_allItemsTable.IsFull()) {
            calcSharedItems();
            try {
                stop();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    private void calcSharedItems() {
        for (byte[] myItem : _allItemsTable.Get(NodeID)) {
            for (int nodeID = 0; nodeID < _countOfAllNodes; nodeID ++) {
                for (byte[] counterpart : _allItemsTable.Get(nodeID)) {
                    if (Arrays.equals(counterpart, myItem)) {
                        _sharedItemsNumber[nodeID] ++;
                    }
                }
            }
        }
        LOG.Info("================Result=================");
        for (int i = 0; i < _sharedItemsNumber.length; i++) {
            LOG.Info("with Node"
                    + i
                    + " shared "
                    + _sharedItemsNumber[i]
                    + " items.");
        }
        LOG.Info("=======================================");
        System.exit(0);
    }

    public void start() throws IOException {
        try {
            sendFirstMessage();
        } catch (NoSuchProviderException e) {
            e.printStackTrace();
        } catch (InvalidKeyException e) {
            e.printStackTrace();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (NoSuchPaddingException e) {
            e.printStackTrace();
        } catch (InvalidAlgorithmParameterException e) {
            e.printStackTrace();
        }
    }

    public void stop() throws InterruptedException {
        _socket.terminate();
    }

    private void sendFirstMessage()
            throws IOException,
            NoSuchProviderException,
            InvalidKeyException,
            NoSuchAlgorithmException,
            NoSuchPaddingException,
            InvalidAlgorithmParameterException {
        List<byte[]> myItems = new LinkedList<byte[]>();
        for (int i = 0; i < _myItems.length; i++) {
            myItems.add(_myItems[i].getBytes("UTF-8"));
        }
        encryptAndShuffle(myItems);
        _socket.send(myItems,
                     1,
                     _allAddresses[(NodeID + 1) % _countOfAllNodes],
                     Message.InProgress);
    }

    private void encryptAndShuffle(List<byte[]> items)
            throws NoSuchPaddingException,
            InvalidKeyException,
            NoSuchAlgorithmException,
            IOException,
            NoSuchProviderException,
            InvalidAlgorithmParameterException {
        Encrypt.cipher(items);

        long seed = System.nanoTime();
        Collections.shuffle(items, new Random(seed));
    }
}
