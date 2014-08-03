import java.net.*; 
import java.io.*; 

public class SocketForNext extends Thread{
	
	private Socket nextSocket = null;
	private int port = 10000;
	private PrintWriter out = null;
	private BufferedReader in = null;
	
	private ObjectInputStream inputStream = null;
	private ObjectOutputStream outputStream = null;
	
	
	public SocketForNext(){
		this.nextSocket = null;
		this.port = 10000;
		this.out = null;
		this.in = null;
		start();
		
	}
	
	public void run(){
		TCPsocket.listenSocket = null; 
		boolean portNumNotFound = true;
		
		
		this.port = TCPsocket.my_port ;
		try {
			TCPsocket.listenSocket = new ServerSocket(port);
			portNumNotFound = false;
		} catch (IOException e1) {
			System.err.println("Could not listen on port:" + port);
			portNumNotFound = true;
		} 
		
		/*
		while (portNumNotFound){
			try { 
				this.port += 1;
				
				TCPsocket.listenSocket = new ServerSocket(port); 
				portNumNotFound = false;
		    } 
		    catch (IOException e){ 
		         System.err.println("Could not listen on port:" + port); 
		         portNumNotFound = true;
		    } 
		}
		*/
		
		System.out.println("IP:Host = " + "127.0.0.1" + ":" + this.port);
		char c = (char) ('A' -1 + (int)(this.port%10));
		TCPsocket.nodeName = "" + c;
		System.out.println("My Node Name : " + TCPsocket.nodeName);
		
	    System.out.println ("Waiting for connection.....");

	    try { 
	    	nextSocket = TCPsocket.listenSocket.accept(); 
	    	PrintWriter out = new PrintWriter(nextSocket.getOutputStream(), true);
			BufferedReader in = new BufferedReader( new InputStreamReader( nextSocket.getInputStream()));
			
			outputStream = new ObjectOutputStream(nextSocket.getOutputStream());
			inputStream = new ObjectInputStream(nextSocket.getInputStream());
			
			
	    } 
	    catch (IOException e) { 
	    	System.err.println("Accept failed."); 
	    	System.exit(1); 
	    } 
	    
	    System.out.println ("[Next Node] Connected!");
	    
	    TCPsocket.nextConnected = true;
	 
	    
	}
	
	
	public void sendObjToNextNode(Msg obj){
			try {
				outputStream.writeObject(obj);
				outputStream.flush();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		
	}
	
	public void sendToNextNode(String msg){
		if (msg != null){
			this.out.println(msg);
			System.out.println("[To Next Node]" + msg);
		}
	}
	
	public void readFromNextNode(){
		String inputLine = null; 
		try {
			inputLine = this.in.readLine();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.out.println("[From Next Node]" + inputLine);
	}
	
	public void closeSocket(){
		
		try {
			out.close(); 
			in.close();
			nextSocket.close(); 
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
	}
	
	public String getMyIP(){
		try{
			String addr = InetAddress.getLocalHost().getHostAddress();
			
			return addr;
		}catch (UnknownHostException e) {
			return null;
		}
	}
}
