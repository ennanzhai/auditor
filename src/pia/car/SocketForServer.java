import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.PrintWriter;
import java.math.BigInteger;
import java.net.ServerSocket;
import java.net.Socket;


public class SocketForServer extends Thread{
	// this socket is used to exchange public keys and get n
	// this is a TCP server socket, wait for the server node to connect
	
	private Socket servSocket = null;
	private ObjectInputStream inputStream = null;
	private ObjectOutputStream outputStream = null;
	
	public SocketForServer(){
		start();
	}
	
	public void run(){
	    System.out.println ("Waiting for Server node connection ....");
	    try { 
	    	servSocket = TCPsocket.listenSocket.accept(); 
			outputStream = new ObjectOutputStream(servSocket.getOutputStream());
			inputStream = new ObjectInputStream(servSocket.getInputStream());
	    } 
	    catch (IOException e) { 
	    	System.err.println("Accept server failed."); 
	    	System.exit(1); 
	    } 
	    
	    System.out.println ("[Server Node] Connected!");
	    
	    
	    
	    // generate public key msg
	    // send to server
	    Msg myPubMsg = Msg.createMyPubKeyMsg(TCPsocket.myData.publicKey);
	    this.sendObjToServerNode(myPubMsg);
	    System.out.print("[To Server] myPubMsg !");
	    
	    this.waitingForServerMsgObj();
	    
	}
	

	

	private void waitingForServerMsgObj(){
		Msg msgIn = null;
		try {
			msgIn = (Msg) inputStream.readObject();
			if (msgIn.type.equals("BigN")){
				// got big n
				processBigNMsg(msgIn);
			}
			
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	private void processBigNMsg(Msg msg){
		TCPsocket.myData.pohli_n = msg.bigB_n;
		TCPsocket.myData.publicKey = msg.pubKey;
		TCPsocket.keysGot = true;
		System.out.println("[From Server] pohli_n = " + TCPsocket.myData.pohli_n);
		System.out.println("[From Server] pubKey = " + TCPsocket.myData.publicKey);
	}
	
	
	public void sendObjToServerNode(Msg obj){
			try {
				outputStream.writeObject(obj);
				outputStream.flush();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		
	}
	
}
