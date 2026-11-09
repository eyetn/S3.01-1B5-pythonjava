import java.util.Scanner;

public class modif_config {

    public static void main() {
        affiche_menu();
        Scanner scan = new Scanner(System.in);
        int choice = scan.nextInt();
        System.out.println(choice);
        while (true) {
            switch (choice) {
            case 1:
                
                break;
            case 2:
                
                break;
            case 3:
                
                break;
            case 4:
                
                break;
            case 5:
                
                break;
            case 0:
                
                break;
        
            default:
                System.out.println("Erreur choisissez parmis :");
                affiche_menu();
                break;
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
}