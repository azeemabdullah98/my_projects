package com.company;
import java.util.*;

public class Main {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Welcome to XYZ Bank");
        boolean cond = true;
        SavingsAccount saveAccount = new SavingsAccount();
        CurrentAccount currAccount = new CurrentAccount();
        while(cond){
            System.out.println("Select any one option from below");
            System.out.print("\n1.Savings Account\n2.Current Account\n3.quit\n");
            int accountChoice = sc.nextInt();
            if(accountChoice == 1){
                saveAccount.run();
            }else if (accountChoice == 2){
                currAccount.run();
            }else if(accountChoice == 3){
                System.out.println("Thank you. Have a Nice day!!!");
                cond=false;
            }
            else{
                System.out.print("\n1.Savings Account\n2.Current Account\n3.quit\n");
                System.out.println("Please select from above options");
                accountChoice = sc.nextInt();
            }
        }
    }
}
