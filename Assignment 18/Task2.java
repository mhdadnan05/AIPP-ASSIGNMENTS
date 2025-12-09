import java.io.*;
import java.util.Scanner;

public class Task2 {
    public static void checkNumber(int num){
        if(num < 0){
            System.out.println("The number is negative");
        }
        else if(number > 0){
            System.out.println("The number is positive");
        }
        else{
            System.out.println("The number is zero");
        }
    }
    public static void main(String args[]){
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter a number: ");
        int number = scanner.nextInt();
        checkNumber(number);
    }
}