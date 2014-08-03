package hbc;

import java.io.*; 
import java.math.BigInteger;
import java.net.*; 
import java.util.ArrayList;
import java.util.Collections;
import java.util.Random;
import java.security.MessageDigest;

import paillierp.PartialDecryption;
import paillierp.zkp.DecryptionZKP;

public class Client {
	private int colludingNum = 1; 
	private int playerNum = 2;
	private int index = -1;
	private ArrayList<BigInteger> inputSet = null;
	private ArrayList<SocketAddress> playerAddrList = null;
	private ArrayList<Socket> playerSocketList = null;
	private ServerSocket serverSocket = null;
	
	public void Client(){
	}
	
	public void connect(){
		try{
			this.connect(InetAddress.getLocalHost().getHostAddress());
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	
	public void connect(String ip) { 
		try {
			System.out.println("connecting " + ip + ":" + Server.PORT);
			Socket peerSocket = new Socket(ip, Server.PORT);
						
			ObjectInputStream in = new ObjectInputStream(peerSocket.getInputStream());
			index = (Integer)in.readObject();
			colludingNum = (Integer)in.readObject();
			playerNum = (Integer)in.readObject();
			System.out.println("Client " + index + " is connect to server");
			
			boolean flag = true;
			int i = 0;
			while(flag){
				try{
					serverSocket = new ServerSocket(Server.PORT + index + i, 19, InetAddress.getLocalHost());
					flag = false;
				}catch(BindException e){
					i = i + 1;
				}
			}
			
			ObjectOutputStream out = new ObjectOutputStream(peerSocket.getOutputStream());
			out.writeObject(serverSocket.getLocalSocketAddress());
		
			flag = true;
			while(flag){
				try{
					in = new ObjectInputStream(peerSocket.getInputStream());
					flag = false;
				}catch(IOException e){
					System.out.println("wait for data");
				}
			}
			playerAddrList = (ArrayList<SocketAddress>)in.readObject();
			System.out.println(playerAddrList);
			
			out.close();
			in.close();
			peerSocket.close(); 
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		
	} 

	
	/**
	 * get input from a file splited by @splitter
	 * @param fileName the input filename
	 * @param splitter the splitter
	 */
	public void getInput(String fileName, String splitter){		
		File inputFile = new File(fileName);
		if(inputFile.exists() == false){
			System.err.println("No such file " + fileName);
		}
		
		FileInputStream fis = null;
		String data = "";
		try{
			File file = new File(fileName);	  
			BufferedReader bf = new BufferedReader(new FileReader(file));
			StringBuilder sb = new StringBuilder();
			String content = "";
			while(content != null){
				sb.append(content);
				content = bf.readLine();
				if (content != null){
					content = content + "\n";
				}
			}
			data = sb.toString();
		}catch(Exception e){
			e.printStackTrace();
		}
		
		String[] datalist = data.split(splitter);
		MessageDigest md = null;
		try{
			md = MessageDigest.getInstance( "MD5" );
		}catch(Exception e){
			e.printStackTrace();
		}
		
		inputSet = new ArrayList<BigInteger>();
		int i = 0;
		for(i = 0; i < datalist.length; i++){
			md.update(datalist[i].getBytes());
			BigInteger tmp = new BigInteger(md.digest());
			inputSet.add( tmp.mod(PaillierPolynomial.scope));
		}
		//System.out.println(data);	
	}

	public void getInput(){
		if (index < 0){
			System.err.println("please connect before get input");
			return ;
		}
		String filename = index  + ".dat";
		getInput(filename, "\n");
	}
	
	/**
	 * send a object to a player by index
	 * @param index the index of player
	 * @param obj the object to send
	 */
	public void sendObjectByIndex(int index, Object obj){
		Socket socket = new Socket();
		try {
			socket.connect(playerAddrList.get(index));
			ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
			out.writeObject(obj);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	/**
	 * recv a object form its serverSocket
	 * @return
	 */
	public Object recvObject(){		
		Object obj = null;	
		try{
		Socket peerSocket = serverSocket.accept();
		ObjectInputStream in = new ObjectInputStream(peerSocket.getInputStream());
		obj = in.readObject();
		}catch(Exception e){
			e.printStackTrace();
		}
		return obj;
	}
	
	/**
	 * @return the size of inter-set
	 */
	public int run(){
		if (index < 0 || playerAddrList == null){
			System.err.println("Please call connect function before run");
			return -1;
		}
		
		if (inputSet == null){
			System.err.println("Please call getInput function before run");
		}				
		
		int i = 0, j = 0;
		// init the paillier 
		PaillierPolynomial paillier = new PaillierPolynomial(index + ".key");
				
		//step 1, cal f
		Polynomial f = new Polynomial(inputSet);		
		Polynomial enc = paillier.encrypt(f);		
		for (i = index + 1; i < index + colludingNum + 1; i++){
			System.out.println("this is " + index + " sending to " + (i % this.playerNum));			
			//sendObjectByIndex(i % this.playerNum, enc);
			sendObjectByIndex(i % this.playerNum, enc);
		}		
		
		System.out.println("Recving ");
		Polynomial theta = paillier.multiply(enc, Polynomial.getRandomPolynomial(f.coefficients.size()));
		for (i = 0; i < this.colludingNum; i++){
			Polynomial encrypt = (Polynomial)recvObject();
			theta = paillier.add(theta, paillier.multiply(encrypt, Polynomial.getRandomPolynomial(f.coefficients.size())));
			//System.out.println("other f = " + paillier.decryptOnly(encrypt).coefficients);
		}
			
		// step 2
		Polynomial p = null;
		if (index == 0){
			Polynomial lamda = theta;
			sendObjectByIndex((index + 1) % playerNum, lamda);
			p = (Polynomial)this.recvObject();
			// step 4
			for (i = 1; i < playerNum; i++){
				sendObjectByIndex(i, p);
			}
		}else{
			// step 3
			Polynomial lamda = (Polynomial)this.recvObject();
			lamda = paillier.add(lamda, theta);
			sendObjectByIndex((index + 1) % playerNum, lamda);
			p = (Polynomial)recvObject(); 
		}
		
		// step 5
		// cal Vi
		ArrayList<BigInteger> valueSet = new ArrayList<BigInteger>(inputSet.size());
		for(i = 0; i < inputSet.size(); i++){
			//System.out.print(inputSet.get(i) + ":");
			BigInteger value = paillier.getValue(p, inputSet.get(i));
			valueSet.add(value);
			//System.out.println(paillier.decryptOnly(value));
		}
		
		// step 6
		ArrayList<BigInteger> allValueSet = null;
		if (index == 0){
			Collections.shuffle(valueSet);
			sendObjectByIndex(1 % playerNum, valueSet);
			allValueSet = (ArrayList<BigInteger>)recvObject();
			// send V to all player
			for (i = 1; i < playerNum; i++){
				sendObjectByIndex(i, allValueSet);
			}
		}else{
			ArrayList<BigInteger> otherValueSet = (ArrayList<BigInteger>)recvObject();
			valueSet.addAll(otherValueSet);
			Collections.shuffle(valueSet);
			sendObjectByIndex((index + 1) % playerNum, valueSet);
			allValueSet = (ArrayList<BigInteger>)recvObject();
		}
		
		//step 6,7
		ArrayList<PartialDecryption> share = paillier.decrypt(allValueSet);
		int count = 0;
		if (index == 0){
			
			ArrayList<ArrayList<PartialDecryption>> shares = new ArrayList<ArrayList<PartialDecryption>>(playerNum);
			for(i = 0; i < share.size(); i++){
				shares.add(new ArrayList<PartialDecryption>());
				shares.get(i).add(share.get(i));
			}
			for(i = 1; i < playerNum; i++){
				ArrayList<PartialDecryption> otherShare = (ArrayList<PartialDecryption>)recvObject();
				for (j = 0; j < otherShare.size(); j++){
					shares.get(j).add(otherShare.get(j));
				}			
			}

			for(i = 0; i < shares.size(); i++){
				if (paillier.combineShares( shares.get(i) ).equals(BigInteger.valueOf(0))){
					count++;
				}
				System.out.println( paillier.combineShares( shares.get(i) ) );
			}
			count = count / playerNum;
			
			for(i = 1; i < playerNum; i++){
				sendObjectByIndex(i, count);
			}			
		}else{
			sendObjectByIndex(0, share);
			count = (Integer)recvObject();
		}
		
		return count;
	}
	
	public static void main(String[] args) { 
		Client client = new Client();
		client.connect();
		client.getInput();
		int count = client.run();
		System.out.println("the size of inter-set is " + count);
	} 
} 
