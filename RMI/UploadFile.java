import java.rmi.Remote;
import java.rmi.RemoteException;

public interface UploadFile extends Remote {
  String uploadFile(String size, byte[] myData) throws RemoteException;
}