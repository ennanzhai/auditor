package com.puncsky.SecureCSI;

public class LOG {

    public static final boolean isDebugging = true;

    public static void Debug(String logMessage) {
        if (isDebugging) {
            System.out.println(logMessage);
        }
    }

    public static void Info(String logMessage) {
        System.out.println(logMessage);
    }
}
