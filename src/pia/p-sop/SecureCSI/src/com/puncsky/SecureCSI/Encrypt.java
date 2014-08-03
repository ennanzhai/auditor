package com.puncsky.SecureCSI;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.Security;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import javax.crypto.Cipher;
import javax.crypto.CipherInputStream;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

/**
 * Encrypt with CTR using AES is commutative and we only support encrypt without
 * decrypt.
 */
public class Encrypt {

    private static byte[] _key = getRandom16Bytes();
    private static byte[] _iv = getRandom16Bytes();

    public static void proveCommutativeEncryption() throws Exception {
        LOG.Info("This is a test to prove "
               + "that it is a commutative encryption.");
        byte[] key1 = getRandom16Bytes();
        byte[] iv1 = getRandom16Bytes();

        byte[] key2 = getRandom16Bytes();
        byte[] iv2 = getRandom16Bytes();

        byte[] input = "puncsky".getBytes();

        byte[] output1 = cipher(key1, iv1, cipher(key2, iv2, input));
        byte[] output2 = cipher(key2, iv2, cipher(key1, iv1, input));

        LOG.Info("Cipher1(Cipher2(data)) == Cipher2(Cipher1(data)) => "
               + (Arrays.equals(output1, output2)));
    }
    
    public static List<byte[]> cipher(List<byte[]> items)
            throws NoSuchPaddingException,
            InvalidAlgorithmParameterException,
            NoSuchAlgorithmException,
            IOException,
            NoSuchProviderException,
            InvalidKeyException {
        for (int i = 0; i < items.size(); i++) {
            byte[] cipher = cipher(items.get(i));
            items.set(i, cipher);
        }
        return items;
    }

    private static byte[] cipher(byte[] data)
            throws NoSuchAlgorithmException,
            NoSuchProviderException,
            NoSuchPaddingException,
            InvalidKeyException,
            InvalidAlgorithmParameterException,
            IOException {
        return cipher(_key, _iv, data);
    }

    private static byte[] cipher(byte[] key, byte[] iv, byte[] data)
            throws NoSuchAlgorithmException,
            NoSuchProviderException,
            NoSuchPaddingException,
            InvalidKeyException,
            InvalidAlgorithmParameterException,
            IOException {
        Security.addProvider(
                new org.bouncycastle.jce.provider.BouncyCastleProvider());
        SecretKeySpec keySpec = new SecretKeySpec(key, "AES");
        IvParameterSpec ivSpec = new IvParameterSpec(iv);
        Cipher cipher = Cipher.getInstance("AES/CTR/NoPadding", "BC");

        // encryption pass
        cipher.init(Cipher.ENCRYPT_MODE, keySpec, ivSpec);
        ByteArrayInputStream bIn = new ByteArrayInputStream(data);
        @SuppressWarnings("resource")
        CipherInputStream cIn = new CipherInputStream(bIn, cipher);
        ByteArrayOutputStream bOut = new ByteArrayOutputStream();

        int ch;
        while ((ch = cIn.read()) >= 0) {
          bOut.write(ch);
        }

        byte[] cipherText = bOut.toByteArray();

        System.out.println("cipher(key: " + new String(key) + ", data: "
                + new String(data) + ") => " + new String(cipherText));

        return cipherText;
    }

    private static byte[] getRandom16Bytes() {
        int size = 16;
        byte[] result= new byte[size];
        Random random= new Random(System.nanoTime());
        random.nextBytes(result);
        return result;
    }
}
