package launcher.view;


import java.io.File;
import java.util.Optional;

import javafx.fxml.FXML;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.Button;
import javafx.scene.control.ButtonType;
import javafx.scene.control.TextField;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import javafx.stage.Window;

public class MainController {
    
    @FXML
    private Stage fenetrePrincipale;

    public void setFenetrePrincipale(Stage stage) {
        this.fenetrePrincipale = stage;
        // l'instruction consume permet d'empêcher de propager l'élément
        this.fenetrePrincipale.setOnCloseRequest(e -> {e.consume();actionQuitter();});
    }

    @FXML 
    private TextField cheminProcessus;
    @FXML 
    private Button btnParcourirProcessus;
    @FXML 
    private TextField cheminRessources;
    @FXML 
    private Button btnParcourirRessources;
    @FXML 
    private TextField cheminEnergie;
    @FXML 
    private Button btnParcourirEnergie;

    @FXML 
    private TextField chpQuantum;

    @FXML 
    private Button btnEnvoi;    

     /** @return la fenetre qui contient cet ecran (pour les boites de dialogue) */
    private Window fenetre() {
        return this.fenetrePrincipale.getOwner();
    }

    private void choisirFichierEntree(TextField champ, String description, String extension) {
        FileChooser choix = new FileChooser();
        choix.setTitle("Choisir un fichier");
        choix.getExtensionFilters().add(new FileChooser.ExtensionFilter(description, extension));
        File actuel = new File(champ.getText());
        if (actuel.getParentFile() != null && actuel.getParentFile().isDirectory()) {
            choix.setInitialDirectory(actuel.getParentFile());
        }
        File fichier = choix.showOpenDialog(fenetre());
        if (fichier != null) {
            champ.setText(fichier.getAbsolutePath());
        }
    }

    public void actionQuitter() {
        Alert confirm = new Alert(AlertType.CONFIRMATION);
        confirm.setTitle("Fermeture de l'appli");
        confirm.setHeaderText("Voulez-vous réellement quitter ?");
        confirm.initOwner(this.fenetrePrincipale);

        ButtonType btnPT = new ButtonType("Plus tard");

        confirm.getButtonTypes().setAll(btnPT, ButtonType.NO, ButtonType.YES);
        Optional<ButtonType> reponse = confirm.showAndWait();
       
        if (reponse.orElse(null) == ButtonType.YES){
            this.fenetrePrincipale.close();
        } else if (reponse.orElse(null) == ButtonType.NO){
            System.out.println("no no no");
        } else if (reponse.orElse(null) == btnPT){
            System.out.println("later...");
        }
    }

}
