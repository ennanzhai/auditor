import java.net.*; 
import java.util.Collections;
import java.io.*; 


public class TCPsocket extends Thread{

	public static boolean prevConnected = false;
	public static boolean nextConnected = false;
	public static boolean keysGot = false;
	public static Data myData = null;
	public static SocketForNext next_socket = null;
	public static SocketForPrev prev_socket = null;
	public static String nodeName = "C";
	public static ServerSocket listenSocket = null; 
	public static int my_port = 0;
	
	// both server socket for the previous node 
	// client socket for the next node
	public static void main(String[] args) throws IOException {
		
		
		
		// if is server, run server code
		if (args.length > 0 && args[0].equals("server")){
			new ServerNode();
			while(true){
				;
			}
			//System.exit(1);
		}
		
		if (args.length > 0){
			my_port = Integer.parseInt(args[0]); //port
		}
		
		
		// open up a new socket to communicate with next node
		next_socket = new SocketForNext();
		try {
		    Thread.sleep(1000);
		} catch (InterruptedException e) {
			
		}
		
		// input previous nodes ip and port to connect
		System.out.println ("Enter IP and Port of previous node (X.X.X.X:XXXX): ");
		BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in));
		String userInput;
		userInput = stdIn.readLine();
		String[] address = userInput.split(":");
		String ipPrev = address[0]; // ip
		int portPrev = Integer.parseInt(address[1]); //port
		
		prev_socket = new SocketForPrev(ipPrev, portPrev);
		
		
		while (!((prevConnected == true) && (nextConnected == true))){
			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
				
			}
		}
		System.out.print("Both connected !");
		// from here connected
		// read in file line by line
		// E(m) encrypt line by line murmur encrypt
		// P(E(m)) shuffle

		myData = new Data(); //also generate pubkey
		myData.readInFile();
		myData.hashMyFile();
		
		
		System.out.print("Wait for server to connect ... ");
		SocketForServer serverSocket = new SocketForServer();
		while (!keysGot){
			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
				
			}
		}
		
		System.out.print("Make sure all nodes get keys. Input 's' to start...");
		userInput = null;
		while((userInput = stdIn.readLine()) != null){
			if (userInput.equals("s")){
				// encrypt my data first
				myData.encryptMyFile();
				myData.shuffleMyEncFile();
				//start create message send to next node
				Msg mymsg = Msg.createMyNewFileMsg();
				next_socket.sendObjToNextNode(mymsg);
				
			}
			if (userInput.equals("c")){
				// start checking the same ones
				int resultNum = myData.getSameNumOfLinesInFinalSet();
			}
			if (userInput.equals("q")){
				//quit
				stdIn.close();
				System.exit(1);
			}
		}
		
	}
	
	
	
	
	
}
