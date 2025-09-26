import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.Map; // <-- Import Map

public interface ExchangeService extends Remote {
    // These methods were already here
    String getDoctorDetails(String doctorId) throws RemoteException;
    String getPatientDetails(String patientId) throws RemoteException;
    String exchangeData(String data) throws RemoteException;

    // Add this missing method definition
    Map<String, Object> exchangebydoctor(int doctorId, int patientId) throws RemoteException;
}