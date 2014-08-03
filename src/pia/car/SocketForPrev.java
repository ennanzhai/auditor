import java.math.BigInteger;
import java.net.*; 
import java.util.ArrayList;
import java.io.*; 

public class SocketForPrev extends Thread {
	
	private Socket prevSocket = null;
    private PrintWriter out = null;
    private BufferedReader in = null;
    private ObjectInputStream inputStream = null;
	private ObjectOutputStream outputStream = null;
	
	
	private String prevNodeIP = "127.0.0.1";
	private int prevNodePort = 0;
	
	public SocketForPrev(String ip, int port){
		this.prevNodeIP = ip;
		this.prevNodePort = port;
		start();
	}
	
	public void sendToPrevNode(String msg){
		 out.println(msg);
		 System.out.println("[To Prev Node]" + msg);
	}
	
	public String readFromPrevNode(){
		String inLine = null;
		try {
			inLine = in.readLine();
			System.out.println("[From Prev Node]" + inLine);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return inLine;
	}
	
	public void closeSocekt(){
		try {
			in.close();
			out.close();
			prevSocket.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public void run(){
	        System.out.println ("Attemping to connect to host " +
			this.prevNodeIP + " on port " + this.prevNodePort + ".");

	        try {
	            this.prevSocket = new Socket(this.prevNodeIP, this.prevNodePort);
	            out = new PrintWriter(this.prevSocket.getOutputStream(), true);
	            in = new BufferedReader(new InputStreamReader(this.prevSocket.getInputStream()));
	            
	            outputStream = new ObjectOutputStream(prevSocket.getOutputStream());
				inputStream = new ObjectInputStream(prevSocket.getInputStream());
				
	        } catch (UnknownHostException e) {
	            System.err.println("Don't know about host: " + this.prevNodeIP);
	            System.exit(1);
	        } catch (IOException e) {
	            System.err.println("Couldn't get I/O for "
	                               + "the connection to: " + this.prevNodeIP);
	            System.exit(1);
	        }
	        System.out.println("[Previous node] connected!");
	        TCPsocket.prevConnected = true;
	        
	        // start waiting for prev node 
	        waitingForPrevNodeMsgObj();

	}
	
	public void gotPassOnToEncryptMsg(Msg msgObj){
		// check if I need to encrypt, 
		if (false == msgObj.encryptedBy.contains(TCPsocket.nodeName)){
			//if yes, encrypt, and pass on to next
			System.out.println("process msg to pass on...");
			ArrayList<BigInteger> enc_cont = TCPsocket.myData.encryptFile(msgObj.content); // encrypt
			msgObj.content = Data.shuffle(enc_cont); // shuffle
			msgObj.encryptedBy.add(TCPsocket.nodeName); // add encrypted by
			TCPsocket.next_socket.sendObjToNextNode(msgObj); // send to next
			
			
		}else{
			// if I have already encrypted, 
			// create DoneEncrypted msg send to next
			System.out.println("Final my message to broadcast...");
			msgObj.type = "DoneEncrypted";
			TCPsocket.myData.insertFinalSet(msgObj.origin, msgObj.content);	// store in Data
			msgObj.whoGot.add(TCPsocket.nodeName); // note i got the file
			TCPsocket.next_socket.sendObjToNextNode(msgObj); // send to next
			
		
		}
	}
	
	public void gotDoneEncryptedMsg(Msg msgObj){
		// check if i got the message before
		// if got, stop pass it on
		// if not, store, add my name into who got and pass on
		if (true == msgObj.whoGot.contains(TCPsocket.nodeName)){
			System.out.println("Stop broadcast.");
		}else{
			System.out.println("Final my message to broadcast...");
			TCPsocket.myData.insertFinalSet(msgObj.origin, msgObj.content);	// store in Data
			msgObj.whoGot.add(TCPsocket.nodeName); // note i got the file
			TCPsocket.next_socket.sendObjToNextNode(msgObj); // send to next
		}
		
	
	}
	/*
	public void pendingMsgFromPrev(String rawMsg){
		// check message
		System.out.println("[From Prev]" + rawMsg);
	}
	*/
	public void pendingMsgObjFromPrev(Msg msgObj){
		// check message
		System.out.println("[From Prev obj]" + msgObj.type );
		if (msgObj.type.equals("PassOnToEncrypt")){
			gotPassOnToEncryptMsg(msgObj);
		}else if (msgObj.type.equals("DoneEncrypted")){
			gotDoneEncryptedMsg(msgObj);
		}else{
			
		}
	}
	
	/*
	// this is for string 
	public void waitingForPrevNodeMsg(){
		String inputLine = null;
		System.out.println("Waiting for prev node to send msg ...");
		try {
			while ((inputLine = in.readLine()) != null){ 
				pendingMsgFromPrev(inputLine);
			}
		} catch (IOException e) {
			e.printStackTrace();
		} 
	}
	*/
	public void waitingForPrevNodeMsgObj(){
		Msg msgIn = null;
		try {
			while((msgIn = (Msg) inputStream.readObject())!= null){
				pendingMsgObjFromPrev(msgIn);
			}
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
