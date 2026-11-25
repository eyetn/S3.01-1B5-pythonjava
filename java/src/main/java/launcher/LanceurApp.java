package launcher;

import java.io.IOException;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.layout.BorderPane;
import javafx.stage.Stage;
import launcher.view.MainController;

public class LanceurApp extends Application{

    private BorderPane rootPane;
	private Stage      primaryStage;
  

    @Override
    public void start(Stage primaryStage) throws Exception {
        
        System.out.println("start");
        
        try {
            FXMLLoader loader = new FXMLLoader();
            loader.setLocation(LanceurApp.class.getResource("config.fxml"));
            BorderPane borderPane = loader.load(); // peut lever IOException

            MainController ctrl = loader.getController();

            Scene scene = new Scene(borderPane);
            primaryStage.setScene(scene);
            primaryStage.setTitle("Ordonnanceur Java-Python");
            primaryStage.show();

            ctrl.setFenetrePrincipale(primaryStage);

            // primaryStage.setOnCloseRequest(e -> actionQuitter(txt));

        } catch (IOException e) {
            System.out.println("Ressource XML non dispo");
            e.printStackTrace();
            System.exit(1);
        }
    }

    @Override
	public void stop() throws Exception {
		System.out.println("Fin de l'application");
	}

    public static void main2(String[] args) {
        launch(args);
    }
}
