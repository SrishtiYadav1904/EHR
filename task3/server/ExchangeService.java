import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.Map;

    public interface ExchangeService extends Remote {
        Map<String, Object> exchangebydoctor(int doctorId, int patientId) throws RemoteException;
    }


