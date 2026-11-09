import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Scanner;

public class modif_config {

    public static void main() {
        Scanner scan = new Scanner(System.in);
        boolean run = true;
        while (run) {
            affiche_menu();
            int choice = scan.nextInt();
            boolean valide = (choice>0 && choice<6);
            if (valide){
                choisir_fic(choice);
            }else if(choice == 0){
                scan.close();
                run = false;
            }else{
                System.out.println("Erreur choissez parmis :");
                continue;
            }
        }
        
    }
       

    private static void affiche_menu(){
        System.out.println("===Menu de configuration===");
        System.out.println("1: Fichier contenant la liste des processus à ordonnancer");
        System.out.println("2: Fichier contenant la description des ressources disponibles");
        System.out.println("3: Fichier(s) dans lequel les résultats de l'ordonnancement");
        System.out.println("4: Fichier dans lequel les métriques globales seront stockées");
        System.out.println("5: Algorithme(s) d'ordonnancement que le programme python exécutera ");
        System.out.println("0: Retour au menu principal");
        System.out.print("\n> ");

    }


    private static void choisir_fic(int type){
        System.out.println("Chemin du fichier");
        System.out.print("\n> ");
        Scanner scan = new Scanner(System.in);
        String path = scan.nextLine();
        scan.close();
        modif("python/ressources/config.txt", path, type);      
    }


    // ! a finir doit permettre la modif
    public static void modif(String path_modif,String new_path,int type) {
        
        try {
            // Création d'un fileReader pour lire le fichier
            FileReader fileReader = new FileReader(path_modif);
            
            // Création d'un bufferedReader qui utilise le fileReader
            BufferedReader reader = new BufferedReader(fileReader);
            
            // une fonction à essayer pouvant générer une erreur
            String line = reader.readLine();
            
            while (line != null) {
                // affichage de la ligne
                System.out.println(line);
                // lecture de la prochaine ligne
                line = reader.readLine();
            }
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}