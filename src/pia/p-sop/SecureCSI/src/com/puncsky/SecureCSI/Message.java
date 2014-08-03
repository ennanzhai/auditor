package com.puncsky.SecureCSI;

import java.io.Serializable;
import java.util.List;

public class Message implements Serializable {

    private static final long serialVersionUID = 1L;

    public static final String InProgress = "InProgress";
    public static final String AllEncrypted = "AllEncrypted";
    
    public Message(String token,
                   int hopCount,
                   int sourceNodeID,
                   List<byte[]> items)
    {
        Token = token;
        HopCount = hopCount;
        SourceNodeID = sourceNodeID;
        Items = items;
    }

    public String Token;
    public int HopCount;
    public int SourceNodeID;
    public List<byte[]> Items;
}
