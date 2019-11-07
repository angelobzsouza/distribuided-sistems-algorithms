import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.rmi.registry.Registry;
import java.rmi.registry.LocateRegistry;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class Server implements UploadFile {
  public Server() {}

  public String uploadFile (String size, byte[] myData) {
    try {
      File serverPathFile = new File("./uploadedFiles/" + size + ".txt");
      FileOutputStream out = new FileOutputStream(serverPathFile);
			
      out.write(myData);
		  out.flush();
      out.close();
		} catch (IOException e) {	
		 	e.printStackTrace();
		}

    return size;
  }

  public static void main(String args[]) { 
    try {
      System.setProperty( "java.rmi.server.hostname", args[0]);
      LocateRegistry.createRegistry(1099);
      Server obj = new Server();
      UploadFile stub = (UploadFile) UnicastRemoteObject.exportObject(obj, 0);    
      Registry registry = LocateRegistry.getRegistry(); 
      registry.bind("UploadFile", stub);
      System.err.println("Server ready"); 
    } catch (Exception e) { 
      System.err.println("Server exception: " + e.toString());
      e.printStackTrace();
    }
  }
}