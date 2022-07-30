package com.company;

import java.util.Scanner;

public abstract class Account {
    int balance;

    public void withdrawMoney(int withdrawAmount){
        if (withdrawAmount>this.balance){
            System.out.println("Insufficient fund, The balance in your selected account is " + this.balance);
        }else{
            this.balance -= withdrawAmount;
            System.out.println("You have withdrawn " + withdrawAmount + " and the balance in your selected account is " + this.balance);
        }
    }

    public void depositMoney(int depositAmount){
        if(depositAmount<0){
            System.out.println("Amount cannot be negative");
        }else{
            this.balance += depositAmount;
            System.out.println("Amount deposited successfully. The balance in your selected account is " + this.balance);
        }
    }

    public void checkBalance(){
    }

    public void run(){
        boolean innerCond = true;
        while(innerCond){
            Scanner sc = new Scanner(System.in);
            System.out.println("Select action from below");
            if (this.balance == 0){
                System.out.println("\n1.deposit\n2.checkBalance\n3.Main menu");
                int choice = sc.nextInt();
                if(choice==1){
                    System.out.println("Specify the amount to deposit");
                    int depositAmount = sc.nextInt();
                    depositMoney(depositAmount);
                }else if(choice == 2){
                    checkBalance();
                }else if (choice == 3){
                    innerCond = false;
                }
            }else{
                System.out.println("\n1.withdraw\n2.deposit\n3.checkBalance\n4.Main menu");
                int choice = sc.nextInt();
                if(choice == 1){
                    System.out.println("Specify the amount to withdraw");
                    int withdrawAmount = sc.nextInt();
                    withdrawMoney(withdrawAmount);
                }else if(choice == 2){
                    System.out.println("Specify the amount to deposit");
                    int depositAmount = sc.nextInt();
                    depositMoney(depositAmount);
                }else if (choice == 3){
                    checkBalance();
                }else if (choice == 4){
                    innerCond = false;
                }
            }
        }
    }
}
