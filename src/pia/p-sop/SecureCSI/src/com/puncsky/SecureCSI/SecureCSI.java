package com.puncsky.SecureCSI;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.InetSocketAddress;
import java.util.LinkedList;
import java.util.List;
import java.util.Properties;
import java.util.Scanner;


public class SecureCSI {

    private static final String AddressConfigFile = "app.config";

    private static final String ItemConfigFile = "items.config";

    /**
     * @param args: Should be only one integer of this node's NodeID.
     * @throws Exception 
     */
    public static void main(String[] args)
            throws Exception {
        if (args.length != 1) {
            DisplayUsage();
            return;
        }
        int myNodeID = Integer.parseInt(args[0]);

        InetSocketAddress[] addresses = LoadAddresses();
        String[] myItems = LoadItems(myNodeID);
        
        Node me = new Node(myNodeID, myItems, addresses);

        LOG.Info("========Press Enter to Continue========");
        Scanner in = new Scanner(System.in);
        String s = in.nextLine();
        me.start();
    }

    private static void DisplayUsage() {
        System.out.println("Usage: SecureCSI <MyNodeID>."
                         + "Please specify the NodeID of this "
                         + "node as the only argument.");
    }

    private static InetSocketAddress[] LoadAddresses() {
        Properties prop = new Properties();
        InputStream input = null;
        List<InetSocketAddress> addresses = new LinkedList<InetSocketAddress>();
        try {
            input = new FileInputStream(AddressConfigFile);
            prop.load(input);
            String address;
            for (Integer i = 0; ; i++) {
                address = prop.getProperty("node" + i.toString());
                if (address == null) {
                    break;
                }
                LOG.Debug("Load address: " + address);
                String[] splits = address.split(":");
                addresses.add(
                    new InetSocketAddress(
                            splits[0], Integer.parseInt(splits[1])));
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        } finally {
            if (input != null) {
                try {
                    input.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        return addresses.toArray(new InetSocketAddress[addresses.size()]);
    }

    private static String[] LoadItems(Integer nodeID) {
        String[] items = null;
        Properties prop = new Properties();
        InputStream input = null;
        try {
            input = new FileInputStream(ItemConfigFile);
            prop.load(input);
            String itemLine = prop.getProperty("node" + nodeID.toString());
            if (itemLine == null || itemLine.isEmpty()) {
                LOG.Debug("Empty items loaded.");
                return new String[0];
            }
            LOG.Debug("Load this node's items: " + itemLine);
            items = itemLine.split(" ");
        } catch (IOException ex) {
            ex.printStackTrace();
        } finally {
            if (input != null) {
                try {
                    input.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        return items;
    }
}
