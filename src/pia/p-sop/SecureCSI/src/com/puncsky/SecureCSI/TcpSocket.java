package com.puncsky.SecureCSI;

import org.apache.commons.lang.SerializationUtils;

import javax.crypto.NoSuchPaddingException;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.util.List;


public class TcpSocket implements Runnable {

    private ServerSocket _listener;

    private Thread _listenerThread;

    private volatile boolean _isRunning = true;

    private Node _node;

    public TcpSocket(Node node, InetSocketAddress socketAddress)
            throws IOException {
        _node = node;

        _listener = new ServerSocket(socketAddress.getPort());
        LOG.Debug(socketAddress.getAddress().toString());
        LOG.Debug(_listener.getLocalSocketAddress().toString());
        _listenerThread = new Thread(this);
        _listenerThread.start();
        LOG.Debug("Listening...");
    }

    /**
     * 
     * @param items: My items to be sent.
     * @param hopCount: The count of hops this message has traveled,
     *                  **including this node**.
     * @param dest: The destination's address.
     * @throws IOException
     */
    public void send(List<byte []> items,
                     int hopCount,
                     InetSocketAddress dest,
                     String messageToken)
            throws IOException {
        Socket socket = new Socket(dest.getAddress(), dest.getPort());
        Message message = new Message(messageToken,
                                      hopCount,
                                      _node.NodeID,
                                      items);
        send(socket, message);
        LOG.Info("Message sent:");
        display(message);
        socket.close();
    }

    /**
     * Send items to all the nodes except myself.
     * @param items
     * @param dests
     * @throws IOException
     */
    public void BroadCast(List<byte []> items,
                          InetSocketAddress[] dests)
            throws IOException {
        LOG.Info("BroadCast the message:");
        for (int i = 0; i < dests.length; i++) {
            if (i != _node.NodeID) {
                send(items, 1, dests[i], Message.AllEncrypted);
            }
        }
    }

    @Override
    public void run() {
        try {
            listen();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
    
    public void terminate() throws InterruptedException {
        _isRunning = false;
        _listenerThread.join();
    }

    private void listen() throws IOException, InterruptedException {
        try {
            while (_isRunning) {
                Socket socket = _listener.accept();
                try {
                    Message msg = recv(socket);

                    LOG.Debug("Message Received:");
                    display(msg);

                    if (msg.Token.equals(Message.InProgress)) {
                        _node.onRecvInProgress(msg.HopCount, msg.Items);
                    } else if (msg.Token.equals(Message.AllEncrypted)) {
                        _node.onRecvAllEncrypted(msg.SourceNodeID,
                                                 msg.Items);
                    } else {
                        LOG.Debug("Unknown message.");
                    }
                } catch (NoSuchAlgorithmException e) {
                    e.printStackTrace();
                } catch (NoSuchPaddingException e) {
                    e.printStackTrace();
                } catch (NoSuchProviderException e) {
                    e.printStackTrace();
                } catch (InvalidKeyException e) {
                    e.printStackTrace();
                } catch (InvalidAlgorithmParameterException e) {
                    e.printStackTrace();
                } finally {
                    socket.close();
                }
            }
        }
        finally {
            terminate();
            _listener.close();
        }
    }

    private Message recv(Socket socket) throws IOException {
        InputStream in = socket.getInputStream();
        DataInputStream dis = new DataInputStream(in);

        int len = dis.readInt();
        byte[] data = new byte[len];
        if (len > 0) {
            dis.readFully(data);
        }

        return (Message) SerializationUtils.deserialize(data);
    }
    
    private void send(Socket socket, Message message) throws IOException {
        byte[] data = SerializationUtils.serialize(message);
        OutputStream os = socket.getOutputStream();
        DataOutputStream dos = new DataOutputStream(os);
        dos.writeInt(data.length);
        dos.write(data, 0, data.length);
        dos.flush();
    }

    private void display(Message msg) {
        LOG.Debug("    Source   : Node" + msg.SourceNodeID);
        LOG.Debug("    Traveled : " + msg.HopCount + " hops");
        LOG.Debug("    Token    : " + msg.Token);
        LOG.Debug("    Items cnt: " + msg.Items.size());
    }
}
