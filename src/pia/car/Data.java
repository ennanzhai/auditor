import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.math.BigInteger;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;
import java.lang.Object;
import java.util.Collection;

public class Data {
	
	public String fileName;
	public ArrayList<String> myFile = null;
	public ArrayList<BigInteger> hashFile = null;
	public ArrayList<BigInteger> encryptedMyFile = null;
	public HashMap<String, ArrayList<BigInteger> > finalSet= null;
	public BigInteger publicKey = BigInteger.ZERO;
	public BigInteger pohli_n = BigInteger.ZERO;
	
	public Data(){
		publicKey = PohligHellman.generateKey();
		//System.out.println("[Data] Public Key = " + publicKey);
		String fname = TCPsocket.nodeName + ".txt";
		this.fileName = this.getClass().getResource(fname).getFile();
		System.out.println("file name:"+this.fileName);
		myFile = new ArrayList<String>();
		hashFile = new ArrayList<BigInteger>();
		encryptedMyFile = new ArrayList<BigInteger>();
		this.finalSet = new HashMap<String, ArrayList<BigInteger> >();
	}
	
	
	
	public void insertFinalSet(String key, ArrayList<BigInteger> content){
		this.finalSet.put(key, content);
		System.out.println("[Data]Stored data " + key + ".");
	}
	
	public void readInFile(){
		System.out.println("[Data] start read in file...");
		System.out.println("[Data]" + this.fileName);
		BufferedReader reader;
		try {
			reader = new BufferedReader(new FileReader(fileName));
			String line = null;
			while ((line = reader.readLine()) != null) {
			    // put in to myFile
				myFile.add(line);
			}
			System.out.println("[Data]read file success !");
		} catch (FileNotFoundException e) {
			System.out.println("[Error] readInFile, file not found!");
		} catch (IOException e) {
			System.out.println("[Error] readInFile, IOException!");
		}
	}
	
	
	
	public void hashMyFile(){
		if (this.hashFile.size() != 0){
			System.out.println("[Data] Already hashed!");
			return;
		}
		for (String line : this.myFile){
			this.hashFile.add(murmurHashString(line));
		}
		System.out.println("[Data] Got my file hashed!");
	}
	
	
	
	
	public void encryptMyFile(){
		if (this.encryptedMyFile.size() != 0 ){
			System.out.println("[Data] Already encrypted!");
			return;
		}
		this.encryptedMyFile = this.encryptFile(this.hashFile);
		System.out.println("[Data] Got my file encrypted!");
		System.out.println("[Test]last line:" + this.encryptedMyFile.get(this.encryptedMyFile.size()-1));
	}
	
	
	public void shuffleMyEncFile(){
		Collections.shuffle(this.encryptedMyFile);
	}
	
	public BigInteger murmurHashString(String str){
		// use murmurhash 64 
		Long hashResult = MurmurHash.hash64(str);
		return new BigInteger(hashResult.toString());
	}
	/*
	public long murmurHashBytes(byte[] data){
		int length = data.length;
		return MurmurHash.hash64(data, length);
	}
	
	public byte[] longToBytes(long x) {
	    ByteBuffer buffer = ByteBuffer.allocate(8);
	    buffer.putLong(x);
	    return buffer.array();
	}

	public long bytesToLong(byte[] bytes) {
	    ByteBuffer buffer = ByteBuffer.allocate(8);
	    buffer.put(bytes);
	    buffer.flip();//need flip 
	    return buffer.getLong();
	}
	*/
	
	public BigInteger encrypt(BigInteger val){
		// todo add PohligHellMan encryption

		BigInteger cipher = PohligHellman.encrypt(val, this.publicKey, this.pohli_n);
		return cipher;
	}
	
	
	public ArrayList<BigInteger> encryptFile(ArrayList<BigInteger> file){
		ArrayList<BigInteger> encFile  = new ArrayList<BigInteger>();
		for (BigInteger val : file){
			encFile.add(encrypt(val));
		}
		return encFile;
	}
	
	public static ArrayList<BigInteger> shuffle(ArrayList<BigInteger> file){
		Collections.shuffle(file);
		return file;
	}
	
	public int getSameNumOfLinesInFinalSet(){
		// return how many are the same
		ArrayList<BigInteger> intersect = cloneList(this.finalSet.values().iterator().next()); // get one value
		for (ArrayList<BigInteger> en_list : this.finalSet.values()){
			intersect.retainAll(en_list);
		}
		int num = intersect.size();
		System.out.println("[Data]Final inersect number = "+ num);
		return num;
	}
	
	public static ArrayList<BigInteger> cloneList(ArrayList<BigInteger> list) {
		ArrayList<BigInteger> clone = new ArrayList<BigInteger>();
	    for(BigInteger item: list){
	    	clone.add(item);
	    } 
	    return clone;
	}
}
